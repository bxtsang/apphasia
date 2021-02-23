import boto3
import json
import os
import requests

client = boto3.client('cognito-idp')
clientSecret = boto3.client('secretsmanager')
hasura_url = os.environ['HASURA_URI']


def lambda_handler(event, context): 
    target = ''
    date = ''
    result = {}
    statusCode = 500
    event = json.loads(event['body'])['input']['eventData']
    hasura_secret = get_secret()
    print(event['recurrence_id'])
    print(event['event_id'])
    print(event['date'])

    try:
        if (event['date'] != None):
            print('recurrence')
            recurrence_id = event['recurrence_id']
            date = event['date']
            target = 'reccurrence'
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
        else:
            print('event')
            target = 'event'
            event_id = event['event_id']
            print(event_id)
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

def get_secret():
    secret_name = "HASURA_ADMIN_SECRET"

    response = clientSecret.get_secret_value(
        SecretId = secret_name
    )


    return json.loads(response['SecretString'])['HASURA_ADMIN_SECRET']