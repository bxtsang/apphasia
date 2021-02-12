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

    statusCode = 500
    parent_folder = os.environ['parent_folder']

    if ('parent_folder' in json.loads(event['body'])) :
        parent_folder = json.loads(event['body'])['parent_folder']


    result = {}
    files = []

    try:
        page_token = None

        while True:
            response = SERVICE.files().list(q=f"'{parent_folder}' in parents",
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name, mimeType, webViewLink, webContentLink)',
                                                pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                files.append(file)
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        result['status'] = "success"
        result['message'] = "successfully retrieved files!"
        result['files'] = files
        statusCode = 200

    except Exception as e:
        result['status'] = "failed"
        result['message'] = "failed to list files"
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
