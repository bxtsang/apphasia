import boto3
import json
import os
import requests

client = boto3.client('cognito-idp')


def lambda_handler(event, context): 
    result = {}
    old_role = ""
    statusCode = 500
    username = json.loads(event['body'])['input']['email']
    user_id = json.loads(event['body'])['input']['user_id']
    current_role = json.loads(event['body'])['input']['current_role']
    new_role = json.loads(event['body'])['input']['new_role']

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
                result['hasura_message'] = "query successfully sent to hasura. refer to result2"
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
