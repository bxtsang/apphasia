import boto3
import json

client = boto3.client('cognito-idp')


def lambda_handler(event, context): 
    print(event)
    result = {}
    statusCode = 500
    previous_password = json.loads(event['body'])['previous_password']
    proposed_password = json.loads(event['body'])['proposed_password']
    access_token = json.loads(event['body'])['access_token']

    try:
        response = client.change_password(
            PreviousPassword=previous_password,
            ProposedPassword=proposed_password,
            AccessToken=access_token
        )
        result['status'] = "success"
        result['message'] = "password changed!!"
        statusCode = 200
    except Exception as e:
        result['status'] = "failed"
        result['message'] = "failed to change password."
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