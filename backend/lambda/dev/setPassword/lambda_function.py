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
    client_id = get_parameter('COGNITO_CLIENT_ID')
    email = json.loads(event['body'])['email']
    code = json.loads(event['body'])['code']
    password = json.loads(event['body'])['password']
    try:
        response = client.confirm_forgot_password(
            ClientId=client_id,
            Username= email,
            ConfirmationCode= code,
            Password= password
        )

        result['status'] = "success"
        result['message'] = "successfully reset password!"
        statusCode = 200
    except Exception as e:
        result['status'] = "error"
        result['message'] = "failed to reset password"
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