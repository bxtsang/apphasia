import boto3
import json
import os
import requests
import base64
from botocore.exceptions import ClientError

client = boto3.client('cognito-idp')


def lambda_handler(event, context): 
    result = {}
    old_role = ""
    statusCode = 500
    username = json.loads(event['body'])['input']['email']
    user_id = json.loads(event['body'])['input']['user_id']
    current_role = json.loads(event['body'])['input']['current_role']
    new_role = json.loads(event['body'])['input']['new_role']

    print(get_secret())
    try:
        response = client.admin_update_user_attributes(
            UserPoolId=os.environ['USER_POOL_ID'],
            Username=username,
            UserAttributes=[
                {
                    'Name': 'custom:role',
                    'Value': new_role
                }
            ]
        )
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
                "x-hasura-admin-secret": os.environ['HASURA_ADMIN_SECRET']
            }

            url = os.environ['HASURA_URI']
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
    secret = ""
    decoded_binary_secret= ""
    secret_name = "HASURA_ADMIN_SECRET"
    region_name = "ap-southeast-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    print("Secret:", secret)
    print("Binary Secret:", decoded_binary_secret) 
    return json.loads(secret)  # returns the secret as dictionary