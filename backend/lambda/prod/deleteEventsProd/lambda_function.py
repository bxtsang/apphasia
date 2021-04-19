import boto3
import json
import os
import requests

client = boto3.client('cognito-idp')
clientSecret = boto3.client('secretsmanager')
client_ssm = boto3.client('ssm')

def lambda_handler(event, context):
    target = ''
    date = ''
    result = {}
    statusCode = 500
    event = json.loads(event['body'])['input']['eventData']
    hasura_secret = get_secret()
    hasura_url = get_parameter("HASURA_URI_PROD")


    try:
        #delete event and onwards
        if (event['date'] != None):
            recurrence_id = event['recurrence_id']
            date = event['date']
            target = f'all events of recurrence id {recurrence_id} from {date} and onwards'
            query = f"""
            mutation {{
                delete_events ( where: {{ _and: {{ recurr_id: {{ _eq: { recurrence_id } }}, date: {{ _gte: "{ date }" }} }} }}
                ) {{
                    affected_rows
                    returning {{
                    id
                    }}
                }}
                }}
            """
        #delete one event
        elif (event['event_id'] != None):
            event_id = event['event_id']
            target = f'event of event id {event_id}'
            query = f"""
            mutation {{
                delete_events(
                    where: {{ id: {{_eq: {event_id} }} }}
                ) {{
                    affected_rows
                    returning {{
                    id
                    }}
                }}
            }}
            """
        #delete ALL events
        elif (event['recurrence_id'] != None):
            recurrence_id = event['recurrence_id']
            target = f'all events of recurrence id {recurrence_id}'
            query = f"""
            mutation {{
                delete_events(
                    where: {{ recurr_id: {{_eq: {recurrence_id} }} }}
                ) {{
                    affected_rows
                    returning {{
                    id
                    }}
                }}
            }}
            """

        else:
            result['status'] = "error"
            result['message'] = "all fields are null "
            return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(result)
            }

        headers = {
            "Content-Type": "application/json",
            "x-hasura-admin-secret": hasura_secret
        }

        r = requests.post(hasura_url, json={'query': query}, headers=headers)
        print(r.status_code)
        print(r.text)

        if r.status_code == 200:
            statusCode = 200
            result['status'] = "sent"
            result['message'] = "successfully deleted " + target
        else:
            statusCode = 400
            result['code'] = r.status_code
            result['status'] = "error"
            result['message'] = "failed to delete " + target


    except Exception as e:
        result['code'] = 400
        result['status'] = "error"
        result['message'] = "failed to delete " + target
        result['error'] = str(e)
        statusCode = 400
        print("error:",e)


    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(result)
    }
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