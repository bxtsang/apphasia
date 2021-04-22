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
    status_code = 500
    drive_id = os.environ['drive_id']
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
        for folder in folders:
            if folder['name'] == old_name:
                file = folder
                print(file)

        if file:
            file = SERVICE.files().update(fileId = file['id'], body = file_metadata).execute()

            result['status'] = "success"
            result['message'] = "file renamed successfully!"
            result['file'] = str(file)
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
