from dateutil.rrule import rrule, MONTHLY, WEEKLY
from dateutil.relativedelta import *
from datetime import date
import requests
import json
import boto3

# ENV VARIABLES
hasura_url = os.environ['HASURA_URI']
hasura_admin_secret = get_secret()

def lambda_handler(event, context):
    # GIVEN VARIABLES
    # project_id = 2
    # recurrence_id = 7
    # start_date = "2021-02-16"
    # new_recurrence = False
    result = {}
    statusCode = 500
    project_id = json.loads(event['body'])['input']['project_id']
    recurrence_id = json.loads(event['body'])['input']['recurrence_id']
    start_date = json.loads(event['body'])['input']['start_date']
    new_recurrence = json.loads(event['body'])['input']['new_recurrence']
    previous_end_date = json.loads(event['body'])['input']['previous_end_date']
    recurrence = json.loads(event['body'])['input']['recurrence']

    # For existing recurrence
    # previous_end_date = "2021-06-10" # OR "YYYY-MM-DD"
    # recurrence = {
    #     "day": 2,
    #     "week": 2,
    #     "interval": 1,
    #     "name": "Doing Dishes",
    #     "frequency": "Monthly",
    #     "end_date": "2021-06-10",
    #     "start_time": "10:00:00",
    #     "end_time": "10:30:00"
    # }

    # CREATE RECURRENCE
    if new_recurrence:
        sql = f"INSERT INTO recurring(day,week,interval,name,frequency,end_date,start_time,end_time) VALUES ({recurrence['day']},{recurrence['week']},{recurrence['interval']},'{recurrence['name']}','{recurrence['frequency']}','{recurrence['end_date']}','{recurrence['start_time']}','{recurrence['end_time']}') RETURNING *;"
    else:
    # SELECT RECURRENCE
        sql = f"SELECT * FROM recurring WHERE id = {recurrence_id};"

    data = json.dumps({
        "type": "run_sql",
        "args": {
            "sql": sql
        }
    })
    res = requests.post(hasura_url,data=data, headers={
    "x-hasura-admin-secret": hasura_admin_secret,
    "Content-Type": "application/json"
    })

    if res.status_code != 200:
        statusCode = res.status_code
        result['status'] = "failed"
        result['message'] = "failed to select/insert recurring"
        return {
            "statusCode": statusCode,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(result)
        }

    recurrence = dict(zip(*res.json()["result"]))

    #COMPUTED VARIABLES
    start_date = date(*[int(ch) for ch in start_date.split("-")])
    end_date = start_date + relativedelta(years=1) if recurrence["end_date"] == "NULL" else date(*[int(ch) for ch in recurrence["end_date"].split("-")])
    events = []
    send = True

    # Create list of events based on its frequency
    if recurrence["frequency"] in ["Weekly","Biweekly"]:
        events = list(rrule(freq=WEEKLY, dtstart=start_date, until=end_date, interval=int(recurrence["interval"])))
    elif recurrence["frequency"] == "Monthly":
        events = list(rrule(freq=MONTHLY, bysetpos=int(recurrence["week"]),byweekday=int(recurrence["day"]), dtstart=start_date, until=end_date ))

    sql = "INSERT INTO events(project_id,date,recurr_id,start_time,end_time,name) VALUES "

    # Create SQL statement for insertion
    if previous_end_date != "NULL":
        previous_end_date = date(*[int(ch) for ch in previous_end_date.split("-")])
        count = 0
        for event in events:
            event = event.date()
            if event > previous_end_date:
                count += 1
                event = event.strftime("%m-%d-%Y")
                sql += f"({project_id},'{event}',{recurrence['id']},'{recurrence['start_time']}','{recurrence['end_time']}','{recurrence['name']}'), "
        if count == 0:
            send = False
    else:
        for event in events:
            event = event.strftime("%m-%d-%Y")
            sql += f"({project_id},'{event}',{recurrence['id']},'{recurrence['start_time']}','{recurrence['end_time']}','{recurrence['name']}'), "

    # Send SQL to database query
    if send:
        sql = sql[:-2] + ";"
        data = json.dumps({
            "type": "run_sql",
            "args": {
                "sql": sql
            }
        })
        res = requests.post(hasura_url,data=data, headers={
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
            statusCode = res.status_code
            result['status'] = "sent"
            result['message'] = "Successfully added events"
    else:
        statusCode = 200
        result['status'] = "sent"
        result['message'] = "No new events to add"

    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(result)
    }

def get_secret():
    secret_name = "HASURA_ADMIN_SECRET"

    response = clientSecret.get_secret_value(
        SecretId = secret_name
    )


    return json.loads(response['SecretString'])['HASURA_ADMIN_SECRET']