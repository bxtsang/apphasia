import boto3
import json

client = boto3.client('cognito-idp')
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
    statusCode = 500
    user_pool_id = get_parameter('USER_POOL_ID')
    email = json.loads(event['body'])['email']

    try:
        response = client.admin_reset_user_password(
            UserPoolId= user_pool_id,
            Username=email
        )

        result['status'] = "success"
        result['message'] = "successfully sent password reset code!"
        statusCode = 200
    except Exception as e:
        result['status'] = "error"
        result['message'] = "failed to send password reset code"
        result['error'] = str(e)
        statusCode = 400
        print("error:",e)

    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin" : "*"
        },
        "body": json.dumps(result)
    }