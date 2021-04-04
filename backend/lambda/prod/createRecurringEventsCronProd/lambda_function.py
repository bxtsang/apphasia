from dateutil.rrule import rrule, MONTHLY, WEEKLY
from dateutil.relativedelta import *
from datetime import *
import requests
import json
import boto3
import os

def get_parameter(parameter):
    response = client_ssm.get_parameter(
    Name=parameter,
    WithDecryption=False
    )

    return response['Parameter']['Value']

def get_secret():
    secret_name = "HASURA_ADMIN_SECRET"

    response = clientSecret.get_secret_value(
        SecretId = secret_name
    )

    return json.loads(response['SecretString'])['HASURA_ADMIN_SECRET']

# ENV VARIABLES
clientSecret = boto3.client('secretsmanager')
client_ssm = boto3.client('ssm')
hasura_url = get_parameter("HASURA_URI_PROD")
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
                    note
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
            if recurrence['infinite']:
                print(createRecurringEvents(recurrence))

        statusCode = 200
        result['status2'] = "success"
        result['message2'] = "Successfully generated events for all recurrences!"

    except Exception as e:
        statusCode = 400
        result['status1'] = "failed"
        result['message1'] = 'Failed to query for recurrences'
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

    end_date =  date(*[int(ch) for ch in recurrence['end_date'].split("-")]) if recurrence['end_date'] else datetime.now().date()
    new_end_date = (datetime.now() + relativedelta(months=6)).date()
    if end_date > new_end_date:
        new_end_date = end_date

    sql = f"SELECT date FROM events WHERE recurr_id = {recurrence['id']} ORDER BY date desc LIMIT 1;"

    query_url = hasura_url[:-7] + "query"

    data = json.dumps({
        "type": "run_sql",
        "args": {"sql": sql}
    })

    try:
        res = requests.post(query_url,data=data, headers={
        "x-hasura-admin-secret": hasura_admin_secret,
        "Content-Type": "application/json"
        })
    except Exception as e:
        statusCode = 400
        result['status'] = "failed"
        result['message'] = f"Failed to get latest events date of recurring id {recurrence['id']}"
        result['error'] = str(e)
        return result


    last_event_date = date(*[int(ch) for ch in res.json()['result'][1][0].split("-")]) if  len(res.json()['result']) > 1 else end_date

    #COMPUTED VARIABLES
    events = []

    # Create list of events based on its frequency
    if recurrence["frequency"] in ["Weekly","Biweekly"]:
        events = list(rrule(freq=WEEKLY, dtstart=recurrence['start_date'], until=new_end_date, interval=int(recurrence["interval"])))
    elif recurrence["frequency"] == "Monthly":
        events = list(rrule(freq=MONTHLY, bysetpos=int(recurrence["week"]),byweekday=int(recurrence["day"]), dtstart=recurrence['start_date'], until=new_end_date, interval=int(recurrence["interval"])))

    sql = "INSERT INTO events(project_id,date,recurr_id,start_time,end_time,name,note) VALUES "

    # Create SQL statement for insertion

    count = 0
    for event in events:
        event = event.date()

        if event > last_event_date:
            count += 1
            event = event.strftime("%m-%d-%Y")
            sql += f"({recurrence['project_id']},'{event}',{recurrence['id']},'{recurrence['start_time']}','{recurrence['end_time']}','{recurrence['name']}','{recurrence['note']}'), "

    send = True if count != 0 else False
    if send:
        # Send SQL to database query
        sql = sql[:-2] + " RETURNING id;"
        data = json.dumps({
            "type": "run_sql",
            "args": {
                "sql": sql
            }
        })

        try:
            res = requests.post(query_url,data=data, headers={
            "x-hasura-admin-secret": hasura_admin_secret,
            "Content-Type": "application/json"
            })
            json_response = json.loads(res.text)
            

            if "errors" not in json_response:
                message = "Successfully added events id "
                events_id = json_response['result']

                for e_id in events_id[1:]:
                    message += e_id[0] + ", "
                message = message[:-2]
                statusCode = 200
                result['status'] = "sent"
                result['message'] = message + f" for recurring id {recurrence['id']}"
            else:
                statusCode = 400
                result['code'] = res.status_code
                result['message'] = res.text
        except Exception as e:
            statusCode = 400
            result['status'] = "failed"
            result['message'] = f"failed to insert into events for recurring id {recurrence['id']}"
            result['error'] = str(e)
            print(str(e))

    else:
        statusCode = 200
        result['status'] = "sent"
        result['message'] = f"No new events to add for recurring id {recurrence['id']}"

    return result
