import json
import boto3
import os
from Google import Create_Service

CLIENT_SECRET_FILE = "aphasiasg.json"
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
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
    drive_id = get_parameter("DRIVE_ID")
    new_folder = json.loads(event['body'])['new_folder']
    parent_folder = ""

    if ('parent_folder' in json.loads(event['body'])) :
        parent_folder = json.loads(event['body'])['parent_folder']

    if parent_folder != "":
        file_metadata = {
            'name': new_folder,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder]
        }
    else:
        file_metadata = {
            'name': new_folder,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [drive_id]
        }

    try:
        folder = SERVICE.files().create(body = file_metadata).execute()

        result['status'] = "success"
        result['message'] = "folder created successfully!"
        result['folderId'] = folder['id']
        result['folderName'] = folder['name']
        statusCode = 200
    except Exception as e:
        result['status'] = "failed"
        result['message'] = "failed to create folder"
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
