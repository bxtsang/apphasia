import json
import os
import boto3
from Google import Create_Service

CLIENT_SECRET_FILE = "aphasiasg.json"
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
client = boto3.client('ssm')

def get_parameter(parameter):
    response = client.get_parameter(
    Name=parameter,
    WithDecryption=False
    )

    return response['Parameter']['Value']

def lambda_handler(event, context):
    print(event)
    result = {}
    status_code = 500
    drive_id = get_parameter("DRIVE_ID")
    folders = []
    new_name = json.loads(event['body'])['event']['data']['new']['title']
    file_id = json.loads(event['body'])['event']['data']['new']['google_drive_id']
    hasura_secret = get_secret()

    print('new_name:', new_name)
    print('file_id:', file_id)

    file_metadata = {
        'name': new_name
    }

    if file_id != "":
        try:
            target_file = SERVICE.files().update(fileId = file_id, body = file_metadata).execute()

            result['status'] = "success"
            result['message'] = "file renamed successfully!"
            result['file'] = str(target_file)
            status_code = 200

        except Exception as e:
            result['status'] = "failed"
            result['message'] = "failed to rename file"
            result['error'] = str(e)
            status_code = 400
    else:
        status_code = 400
        result['status'] = "error"
        result['message'] = "empty project id column in database"

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(result)
    }