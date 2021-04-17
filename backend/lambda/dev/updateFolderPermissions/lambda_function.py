import json
import os
import boto3
import requests
from Google import Create_Service

CLIENT_SECRET_FILE = "aphasiasg.json"
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
client_ssm = boto3.client('ssm')
client_secret = boto3.client('secretsmanager')
result = {}
folder_error = ""
permission_errors = ""
hasura_error = ""
update_drive_error = ""

def get_parameter(parameter):
    response = client_ssm.get_parameter(
    Name=parameter,
    WithDecryption=False
    )

    return response['Parameter']['Value']

def remove_permission(emails, file_id):
    return

def add_permission(emails, file_id):
    try:
        result['message'] = "file permissions added for "
        for email in emails:
            file_metadata = {
                "role": "writer",
                "type": "user",
                "emailAddress": email
            }
            SERVICE.permissions().create(fileId=file_id, body = file_metadata).execute()
            result['message'] += email + ", "
        result['status'] = "success"
        statusCode = 200
        return True

    except Exception as e:
        permission_errors = str(e)
        print(str(e))
        return False


def get_secret(secret_name):

    response = client_secret.get_secret_value(
        SecretId = secret_name
    )


    return json.loads(response['SecretString'])[secret_name]

def lambda_handler(event, context):
    print("event:", event)
    statusCode = 500

    file_id = ""
    new_folder = json.loads(event['body'])['event']['data']['new']['title']
    project_id = json.loads(event['body'])['event']['data']['new']['id']

    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(result)
    }
