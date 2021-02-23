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


    if eventsOrRecurring["recurringData"]['frequency'] == "None":

        headers = {
                "Content-Type": "application/json",
                "x-hasura-admin-secret": hasura_secret
            }
        eventsOrRecurring.pop("recurringData", None)
        eventsOrRecurring['date'] = eventsOrRecurring.pop("start_date", None)
        data = {'event': eventsOrRecurring}
        query = f"""mutation InsertSingleEvent($event: events_insert_input!) {{
                insert_events_one(object: $event) {{
                    id
                }}
            }}
              """
        r = requests.post(hasura_url, json={'query': query, "variables": data}, headers=headers)
        print(r.status_code)
        print(r.text)

        if r.status_code == 200:
            statusCode = 200
            result['status'] = "sent"
            result['message'] = "query successfully sent to hasura"
        else:
            statusCode = 400
            result['code'] = r.status_code
            result['message'] = "query failed to sent to hasura"
        
    else:
        pass

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
