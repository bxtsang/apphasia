import json
import os
from Google import Create_Service

CLIENT_SECRET_FILE = "aphasiasg.json"
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def lambda_handler(event, context):
    print(event)
    result = {}
    statusCode = 500
    file_id = json.loads(event['body'])['file_id']
    new_name = json.loads(event['body'])['new_name']

    file_metadata = {
        'name': new_name
    }

    try:
        file = SERVICE.files().update(fileId = file_id, body = file_metadata).execute()

        result['status'] = "success"
        result['message'] = "file renamed successfully!"
        result['file'] = str(file)
        statusCode = 200

    except Exception as e:
        result['status'] = "failed"
        result['message'] = "failed to rename file"
        result['error'] = str(e)
        statusCode = 400

    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(result)
    }
