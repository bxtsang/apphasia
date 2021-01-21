import boto3
import json

client = boto3.client('cognito-idp')


def lambda_handler(event, context): 
    print(event
    )
    result = {}
    statusCode = 500
    access_token = json.loads(event['body'])['access_token']
    code = json.loads(event['body'])['code']
    try:
        response = client.verify_user_attribute(AccessToken= access_token,AttributeName= "email",Code= code)
        result['status'] = "success"
        result['message'] = "successfully verified email!"
        statusCode = 200
    except Exception as e:
        response = client.get_user_attribute_verification_code(
    AccessToken=access_token,
    AttributeName='email'
)
        result['status'] = "failed"
        result['message'] = "failed to verify email, new verification code sent to user"
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