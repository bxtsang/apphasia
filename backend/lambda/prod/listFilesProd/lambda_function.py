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

    statusCode = 500
    parent_folder = get_parameter('DRIVE_ID')

    if ('parent_folder' in json.loads(event['body'])) :
        if not json.loads(event['body'])['parent_folder'] == "":
            parent_folder = json.loads(event['body'])['parent_folder']


    result = {}
    files = []

    try:
        page_token = None

        while True:
            response = SERVICE.files().list(q=f"'{parent_folder}' in parents",
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name, mimeType, webViewLink, webContentLink, thumbnailLink, iconLink)',
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