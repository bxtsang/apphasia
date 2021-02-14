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
    drive_id = os.environ['drive_id']
    file_id = json.loads(event['body'])['file_id']
    old_parent = drive_id
    new_parent = drive_id

    if 'old_parent' in json.loads(event['body']) and not json.loads(event['body'])['old_parent'] == "":
        old_parent = json.loads(event['body'])['old_parent']

    if 'new_parent' in json.loads(event['body']) and not json.loads(event['body'])['new_parent'] == "":
        new_parent = json.loads(event['body'])['new_parent']

    try:
        file = SERVICE.files().update(fileId = file_id , addParents=new_parent, removeParents=old_parent).execute()
        print(file)

        result['status'] = "success"
        result['message'] = "file moved successfully!"
        result['fileName'] = file['name']
        result['fileId'] = file['id']
        statusCode = 200

    except Exception as e:
        result['status'] = "failed"
        result['message'] = "failed to move file"
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
