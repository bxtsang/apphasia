import json
import os
from Google import Create_Service

CLIENT_SECRET_FILE = "credentials.json"
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def lambda_handler(event, context):
    print(event)
    result = {}
    statusCode = 500
    fileId = json.loads(event['body'])['fileId']

    try:
        SERVICE.files().delete(fileId=fileId).execute()
        result['status'] = "success"
        result['message'] = "folder deleted successfully!"
        statusCode = 200

    except Exception as e:
        result['status'] = "failed"
        result['message'] = "failed to delete folder"
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
