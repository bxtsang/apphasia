import json
import os
from Google import Create_Service
from googleapiclient.http import MediaFileUpload

CLIENT_SECRET_FILE = "aphasiasg.json"
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def lambda_handler(event, context):
    print(event)

    statusCode = 500

    # folder_id = json.loads(event['body'])['folder_id']

    folder_id = ""

    file_names = []
    mimeTypes = []

    result = {}
    files = []

    try:

        for file_name in file_names:
            file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }

        

        result['status'] = "success"
        result['message'] = "successfully uploaded file!"
        result['files'] = files
        statusCode = 200

    except Exception as e:
        result['status'] = "failed"
        result['message'] = "failed to upload file"
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
