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
    old_name = json.loads(event['body'])['event']['data']['old']['title']
    new_name = json.loads(event['body'])['event']['data']['new']['title']

    print('old_name:', old_name)
    print('new_name:', new_name)

    file_metadata = {
        'name': new_name
    }

    try:
        page_token = None

        while True:
            response = SERVICE.files().list(q=f"'{drive_id}' in parents",
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name, mimeType, webViewLink, webContentLink, thumbnailLink, iconLink)',
                                                pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                folders.append(file)
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    except Exception as e:
        result['status'] = "failed"
        result['message'] = "failed to list files"
        result['error'] = str(e)
        status_code = 400

    try:
        target_file = None
        for folder in folders:
            if folder['name'] == old_name:
                target_file = folder
                print(target_file)

        if target_file != None:
            target_file = SERVICE.files().update(fileId = target_file['id'], body = file_metadata).execute()

            result['status'] = "success"
            result['message'] = "file renamed successfully!"
            result['file'] = str(target_file)
            status_code = 200

        else:
            result['status'] = "failed"
            result['message'] = "file not found"
            status_code = 400

    except Exception as e:
        result['status'] = "failed"
        result['message'] = "failed to rename file"
        result['error'] = str(e)
        status_code = 400

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(result)
    }
