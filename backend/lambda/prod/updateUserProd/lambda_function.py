import boto3
import json
import os
import requests
import base64
from botocore.exceptions import ClientError

client_cognito = boto3.client('cognito-idp')
client_secret = boto3.client('secretsmanager')
client_ssm = boto3.client('ssm')

def get_parameter(parameter):
    response = client_ssm.get_parameter(
    Name=parameter,
    WithDecryption=False
    )

    return response['Parameter']['Value']

def lambda_handler(event, context):
    print(event)
    result = {}
    old_role = ""
    statusCode = 500
    username = json.loads(event['body'])['input']['email']
    user_id = json.loads(event['body'])['input']['user_id']
    current_role = json.loads(event['body'])['input']['current_role']
    new_role = json.loads(event['body'])['input']['new_role']
    hasura_secret = get_secret()
    user_pool_id = get_parameter('USER_POOL_ID')

    try:
        response = client_cognito.admin_update_user_attributes(
            UserPoolId=user_pool_id,
            Username=username,
            UserAttributes=[
                {
                    'Name': 'custom:role',
                    'Value': new_role
                }
            ]
        )
        result['status'] = "success"
        result['message'] = "successfully updated user!"
        statusCode = 200

    except Exception as e:
        result['status'] = "failed"
        result['message'] = "failed to udpate user."
        result['error'] = str(e)
        statusCode = 400
        print("error:",e)

        try:
            query = f"""mutation {{
            update_staffs (
                where: {{ id: {{_eq: {user_id} }} }},
                _set: {{
                role: {current_role}
                }}
            ) {{
                affected_rows
                returning {{
                id
                name
                role
                email
                }}
            }}
            }}
              """

            headers = {
                "Content-Type": "application/json",
                "x-hasura-admin-secret": hasura_secret
            }

            url = get_parameter("HASURA_URI")
            r = requests.post(url, json={'query': query}, headers=headers)
            print(r.status_code)
            print(r.text)

            if r.status_code == 200:
                result['hasura_status'] = "sent"
                result['hasura_message'] = "query successfully sent to hasura. refer to hasura_result"
                result['hasura_result'] = r.text
            else:
                result['hasura_status'] = "failed"
                result['hasura_message'] = "failed to send query to hasura"
                result['hasura_result'] = r.text

        except Exception as e:
                print(e)
                result['hasura_status'] = "failed"
                result['hasura_message'] = "failed to send query to hasura"
                result['hasura_error'] = str(e)

    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(result)
    }



def get_secret():
    secret_name = "HASURA_ADMIN_SECRET"

    response = client_secret.get_secret_value(
        SecretId = secret_name
    )


    return json.loads(response['SecretString'])['HASURA_ADMIN_SECRET']
