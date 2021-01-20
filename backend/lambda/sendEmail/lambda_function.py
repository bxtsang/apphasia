import boto3
import json

client = boto3.client('cognito-idp')


def lambda_handler(event, context): 
    print(event)
    result = {}
    statusCode = 500
    access_token = event['access_token']

    try:
        response = client.get_user_attribute_verification_code(
    AccessToken=access_token,
    AttributeName='email'
)
        result['status'] = "success"
        result['message'] = "verification code sent!"
        statusCode = 200
    except Exception as e:
        result['status'] = "failed"
        result['message'] = "failed to send verification code."
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