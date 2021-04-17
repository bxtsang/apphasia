import json
import os
import boto3
import requests
from Google import Create_Service

CLIENT_SECRET_FILE = "aphasiasg.json"
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
client_ssm = boto3.client('ssm')
client_secret = boto3.client('secretsmanager')
result = {}
folder_error = ""

def get_parameter(parameter):
    response = client_ssm.get_parameter(
    Name=parameter,
    WithDecryption=False
    )

    return response['Parameter']['Value']

def create_folder(new_folder):
    drive_id = get_parameter("DRIVE_ID")
    file_metadata = {
        'name': new_folder,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [drive_id]
    }

    try:
        folder = SERVICE.files().create(body = file_metadata).execute()
        result['message'] = f"folder created with id {folder['id']}"
        return folder['id']

    except Exception as e:
        folder_error = str(e)
        print(str(e))
        return ""

def get_secret(secret_name):

    response = client_secret.get_secret_value(
        SecretId = secret_name
    )


    return json.loads(response['SecretString'])[secret_name]

def update_drive_id(file_id, project_id):
    HASURA_URI = "https://aphasia-hasura-dev.herokuapp.com/v1/graphql"
    HASURA_ADMIN_SECRET = get_secret("HASURA_ADMIN_SECRET")
    HASURA_HEADERS = { "Content-Type": "application/json", "x-hasura-admin-secret": HASURA_ADMIN_SECRET }
    success = True
    query = f"""
    mutation{{
        update_projects_by_pk (pk_columns: {{id: {project_id}}} _set: {{google_drive_id: "{file_id}"}}) {{
            id
            google_drive_id
        }}
    }}
    """
    try:
        r = requests.post(HASURA_URI, json = {'query' : query}, headers = HASURA_HEADERS)

        if r.status_code != 200:
            update_drive_error = r.text
            print(r.text)
            success = False
        else:
            print(r.text)

    except Exception as e:
        update_drive_error = e
        print(str(e))
        success = False

    return success

def lambda_handler(event, context):
    print("event:", event)
    statusCode = 500

    file_id = ""
    new_folder = json.loads(event['body'])['event']['data']['new']['title']
    project_id = json.loads(event['body'])['event']['data']['new']['id']

    print("new folder name:", new_folder)
    file_id = create_folder(new_folder)
    update_drive_id(file_id, project_id)

    if file_id == "":
        statusCode = 400 
        result['status'] = "error"
        result['message'] = "failed to add project folder"
        result['error'] = folder_error
        return {
            "statusCode": statusCode,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(result)
        }

    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(result)
    }
