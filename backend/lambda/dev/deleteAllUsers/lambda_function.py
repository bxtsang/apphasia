import boto3
import json
import os

client = boto3.client('cognito-idp')

def lambda_handler(event, context):
    result = {}
    statusCode = 500

    try:
        response = client.list_users(
            UserPoolId=os.environ['USER_POOL_ID'],
            AttributesToGet=[
                'email',
            ]
        )
        print(response)

        for user in response['Users']:
            response = client.admin_delete_user(
                UserPoolId=os.environ['USER_POOL_ID'],
                Username=user['Username']
            )
            print(user['Username'])
            print(response)

        result['message'] = "successfully deleted users!"
        statusCode = 200

    except Exception as e:
        result['status'] = "error"
        result['message'] = "failed to delete users"
        result['error'] = str(e)
        statusCode = 400
        print("error:",e)


    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(result)
    }
