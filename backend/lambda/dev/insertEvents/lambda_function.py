from dateutil.rrule import rrule, MONTHLY, WEEKLY
from dateutil.relativedelta import *
from datetime import date
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
    
    # GIVEN VARIABLES 
    # project_id = 2 OR null
    # recurrence_id = 7
    # day = 1
    # week = 2 OR null
    # interval = 1
    # name = Test
    # frequency = "Weekly" OR "Monthly"
    # start_date = "2021-02-16"
    # end_date = "2022-02-14" or NULL
    # start_time = "13:00:00+00"
    # end_time = 14:00:00+00"
    # infinite = false
    # notes = "test" or ""
    recurrence = json.loads(event['body'])['event']['data']['new']
    result = {}
    statusCode = 500
    recurrence['start_date'] = date(*[int(ch) for ch in recurrence['start_date'].split("-")])
    recurrence['project_id'] = recurrence['project_id'] if recurrence['project_id'] else "NULL"

    if recurrence['end_date']:
        recurrence['end_date'] = date(*[int(ch) for ch in recurrence['end_date'].split("-")])
    else:
        recurrence['end_date'] = recurrence['start_date'] + relativedelta(years=1)
        sql = f"UPDATE recurring SET end_date = '{recurrence['end_date'].strftime('%m-%d-%Y')}', infinite = true WHERE id = {recurrence['id']};"
        data = json.dumps({
            "type": "run_sql",
            "args": {"sql": sql}
        })
        try:
            res = requests.post(hasura_url,data=data, headers={
            "x-hasura-admin-secret": hasura_admin_secret,
            "Content-Type": "application/json"
            })
        except Exception as e:
            statusCode = res.status_code
            result['status'] = "failed"
            result['message'] = "failed to update end_date"
            result['error'] = str(e)
            return {
                "statusCode": statusCode,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(result)
            }

    #COMPUTED VARIABLES
    events = []

    # Create list of events based on its frequency
    if recurrence["frequency"] in ["Weekly","Biweekly"]:
        events = list(rrule(freq=WEEKLY, dtstart=recurrence['start_date'], until=recurrence['end_date'], interval=int(recurrence["interval"])))
    elif recurrence["frequency"] == "Monthly":
        events = list(rrule(freq=MONTHLY, bysetpos=int(recurrence["week"]),byweekday=int(recurrence["day"]), dtstart=recurrence['start_date'], until=recurrence['end_date'], interval=int(recurrence["interval"])))

    sql = "INSERT INTO events(project_id,date,recurr_id,start_time,end_time,name,note) VALUES "

    # Create SQL statement for insertion

    for event in events:
        event = event.strftime("%m-%d-%Y")
        sql += f"({recurrence['project_id']},'{event}',{recurrence['id']},'{recurrence['start_time']}','{recurrence['end_time']}','{recurrence['name']}','{recurrence['note']}'), "

    # Send SQL to database query
    sql = sql[:-2] + ";"
    data = json.dumps({
        "type": "run_sql",
        "args": {
            "sql": sql
        }
    })

    try:
        res = requests.post(hasura_url,data=data, headers={
        "x-hasura-admin-secret": hasura_admin_secret,
        "Content-Type": "application/json"
        })

        json_response = json.loads(res.text)

        if "errors" not in json_response:
            statusCode = 200
            result['status'] = "sent"
            result['message'] = "Successfully added events"
        else:
            statusCode = 400
            result['code'] = res.status_code
            result['message'] = res.text
    except Exception as e:
        statusCode = 400
        result['status'] = "failed"
        result['message'] = "failed to add to events"
        result['error'] = str(e)

    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(result)
    }
