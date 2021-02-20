from dateutil.rrule import rrule, MONTHLY, WEEKLY
from dateutil.relativedelta import *
from datetime import *
import requests
import json
import boto3
import os

def get_secret():
    secret_name = "HASURA_ADMIN_SECRET"

    response = clientSecret.get_secret_value(
        SecretId = secret_name
    )

    return json.loads(response['SecretString'])['HASURA_ADMIN_SECRET']

# ENV VARIABLES
clientSecret = boto3.client('secretsmanager')
hasura_url = os.environ['HASURA_URI']
hasura_admin_secret = get_secret()

def lambda_handler(event, context):
    result = {}
    statusCode = 500

    try:
        query = f"""{{
                recurring {{
                    day
                    end_date
                    end_time
                    id
                    project_id
                    start_date
                    start_time
                    name
                    infinite
                    interval
                    frequency
                    week
                }}
                }}
            """

        headers = {
            "Content-Type": "application/json",
            "x-hasura-admin-secret": hasura_admin_secret
        }

        r = requests.post(hasura_url, json={'query': query}, headers=headers)
        result['status1'] = "success"
        result['message1'] = "successfully queried for recurrences"

        recurrences = json.loads(r.text)['data']['recurring']
        for recurrence in recurrences:
            print(recurrence)
            if recurrence['infinite']:
                print(createRecurringEvents(recurrence))

        statusCode = 200
        result['status2'] = "success"
        result['message2'] = "successfully generated events!"

    except Exception as e:
        statusCode = 400
        result['status1'] = "failed"
        result['message1'] = 'failed to query for recurrences'
        result['error1'] = str(e)
        print(str(e))




    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(result)
    }

def createRecurringEvents (recurrence):
    result = {}
    statusCode = 500
    recurrence['start_date'] = date(*[int(ch) for ch in recurrence['start_date'].split("-")])
    recurrence['project_id'] = recurrence['project_id'] if recurrence['project_id'] else "NULL"

    end_date =  date(*[int(ch) for ch in recurrence['end_date'].split("-")])
    new_end_date = (datetime.now() + relativedelta(months=6)).date()
    if end_date > new_end_date:
        new_end_date = end_date

    sql = f"SELECT date FROM events WHERE recurr_id = {recurrence['id']} ORDER BY date desc LIMIT 1;"

    query_url = hasura_url[:-7] + "query"

    data = json.dumps({
        "type": "run_sql",
        "args": {"sql": sql}
    })
    res = requests.post(query_url,data=data, headers={
    "x-hasura-admin-secret": hasura_admin_secret,
    "Content-Type": "application/json"
    })

    if res.status_code != 200:
        result['status_code'] = res.status_code
        result['status'] = "failed"
        result['message'] = "Failed to get latest events date"
        return result

    last_event_date = date(*[int(ch) for ch in res.json()['result'][1][0].split("-")]) if  len(res.json()['result']) > 1 else end_date

    #COMPUTED VARIABLES
    events = []

    # Create list of events based on its frequency
    if recurrence["frequency"] in ["Weekly","Biweekly"]:
        events = list(rrule(freq=WEEKLY, dtstart=recurrence['start_date'], until=new_end_date, interval=int(recurrence["interval"])))
    elif recurrence["frequency"] == "Monthly":
        events = list(rrule(freq=MONTHLY, bysetpos=int(recurrence["week"]),byweekday=int(recurrence["day"]), dtstart=recurrence['start_date'], until=new_end_date, interval=int(recurrence["interval"])))

    sql = "INSERT INTO events(project_id,date,recurr_id,start_time,end_time,name) VALUES "

    # Create SQL statement for insertion

    count = 0
    for event in events:
        event = event.date()

        if event > last_event_date:
            count += 1
            event = event.strftime("%m-%d-%Y")
            sql += f"({recurrence['project_id']},'{event}',{recurrence['id']},'{recurrence['start_time']}','{recurrence['end_time']}','{recurrence['name']}'), "

    send = True if count != 0 else False
    if send:
        # Send SQL to database query
        sql = sql[:-2] + ";"
        data = json.dumps({
            "type": "run_sql",
            "args": {
                "sql": sql
            }
        })
        res = requests.post(query_url,data=data, headers={
        "x-hasura-admin-secret": hasura_admin_secret,
        "Content-Type": "application/json"
        })

        # result['message'] = json.dumps(res.json())
        # statusCode = 200
        if res.status_code != 200:
            statusCode = res.status_code
            result['status'] = "failed"
            result['message'] = "Failed to insert into Events."
        else:
            statusCode = 200
            statusCode = res.status_code
            result['status'] = "sent"
            result['message'] = "Successfully added events" 
    else:
        statusCode = 200
        result['status'] = "sent"
        result['message'] = "No new events to add"

    return result
