import boto3
import json
import os
import requests

client = boto3.client('cognito-idp')
clientSecret = boto3.client('secretsmanager')
hasura_url = os.environ['HASURA_URI']

def lambda_handler(event, context):
    result = {}
    statusCode = 500
    eventsOrRecurring = json.loads(event['body'])['input']['newEventData']
    hasura_secret = get_secret()

    headers = {
            "Content-Type": "application/json",
            "x-hasura-admin-secret": hasura_secret
        }

    if eventsOrRecurring["recurringData"]['frequency'] == "None":
        eventsOrRecurring.pop("recurringData", None)
        eventsOrRecurring['date'] = eventsOrRecurring.pop("start_date", None)
        data = {'event': eventsOrRecurring}
        query = f"""mutation InsertSingleEvent($event: events_insert_input!) {{
                insert_events_one(object: $event) {{
                    id
                }}
            }}
              """

    else:
        eventsOrRecurring = {**eventsOrRecurring,**eventsOrRecurring['recurringData']}
        if eventsOrRecurring['end_date'] == "":
            eventsOrRecurring["end_date"] = None
        del eventsOrRecurring['recurringData']
        data = {'recurring': eventsOrRecurring}
        query = f"""
        mutation InsertEvents($recurring: recurring_insert_input!) {{
            insert_recurring_one(object: $recurring) {{
                id
            }}
        }}
        """

    r = requests.post(hasura_url, json={'query': query, "variables": data}, headers=headers)
    print(r.status_code)
    print(r.text)
    json_response = json.loads(r.text)

    if "errors" not in json_response:
        statusCode = 200
        result['status'] = "sent"
        result['message'] = "query successfully sent to hasura"
    else:
        statusCode = 400
        result['code'] = r.status_code
        result['message'] = r.text

    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(result)
    }




def get_secret():
    secret_name = "HASURA_ADMIN_SECRET"

    response = clientSecret.get_secret_value(
        SecretId = secret_name
    )


    return json.loads(response['SecretString'])['HASURA_ADMIN_SECRET']
