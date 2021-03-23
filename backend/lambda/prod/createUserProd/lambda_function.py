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
    role = json.loads(event['body'])['input']['role']
    user_id = json.loads(event['body'])['input']['user_id']
    email = json.loads(event['body'])['input']['email']
    password = json.loads(event['body'])['input']['password']
    hasura_secret = get_secret()
    user_pool_id = get_parameter('USER_POOL_ID')
    client_id = get_parameter('COGNITO_CLIENT_ID')

    try:
        response = client_cognito.sign_up(
            ClientId= client_id,
            Username= email,
            Password= password,
            UserAttributes=[
                {
                    'Name': 'custom:role',
                    'Value': role
                },
            ],
            ValidationData=[
                {
                    'Name': 'custom:hasura_id',
                    'Value': str(user_id)
                },
            ]
        )

        result['status'] = "success"
        result['message'] = "successfully created user!"
        statusCode = 200

    except Exception as e:
        result['status'] = "failed"
        result['message'] = "failed to create user."
        result['error'] = str(e)
        statusCode = 400
        print("error:",e)

        if str(e) != "An error occurred (UsernameExistsException) when calling the SignUp operation: An account with the given email already exists.":
            try:
                query = f"""mutation {{
                    delete_staffs (
                        where: {{
                        id: {{
                            _eq: {user_id}
                        }}
                        }}
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

                url = get_parameter("HASURA_URI_PROD")
                r = requests.post(url, json={'query': query}, headers=headers)
                print(r.status_code)
                print(r.text)

                if r.status_code == 200:
                    result['hasura_status'] = "success"
                    result['hasura_result'] = r.text
                else:
                    result['hasura_status'] = "error"
                    result['hasura_result'] = r.text

            except Exception as e:
                    print(e)
                    result['hasura_status'] = "error"
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
