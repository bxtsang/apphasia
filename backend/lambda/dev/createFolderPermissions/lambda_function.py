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
result = {}

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


def lambda_handler(event, context):
    print("event:", event)
    result = {}
    statusCode = 500

    file_id = json.loads(event['body'])['file_id']
    emails = json.loads(event['body'])['emails']

    if (len(emails) <= 0):
        result['status'] = "error"
        result['message'] = "email list cannot be empty!"
        statusCode = 400

        return {
            "statusCode": statusCode,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(result)
         }
     
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

    except Exception as e:
        result['status'] = "error"
        result['message'] = "failed to add file permission for all users"
        result['error'] = str(e)
        print("error", str(e))
        statusCode = 400

    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(result)
    }
