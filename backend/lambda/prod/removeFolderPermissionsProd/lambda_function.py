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
client = boto3.client('ssm')
result = {}
client_ssm = boto3.client('ssm')
client_secret = boto3.client('secretsmanager')
result = {}
error_list = []

def get_parameter(parameter):
    response = client_ssm.get_parameter(
    Name=parameter,
    WithDecryption=False
    )

    return response['Parameter']['Value']

def get_secret(secret_name):

    response = client_secret.get_secret_value(
        SecretId = secret_name
    )


    return json.loads(response['SecretString'])[secret_name]

def remove_permission(email, file_id):
    file_metadata = {
                "role": "writer",
                "type": "user",
                "emailAddress": email
            }

    try:
        permission_list = SERVICE.permissions().list(fileId=file_id, fields="permissions(id, emailAddress)").execute()['permissions']
        for permission in permission_list:
            if permission['emailAddress'] == email:
                print("permission found:", permission)
                permission_id = permission['id']
                SERVICE.permissions().delete(fileId=file_id, permissionId=permission_id).execute()
                return True
        return False

    except Exception as e:
        error_list.append(str(e))
        print(str(e))
        return False

def get_google_drive_id (project_id):
    HASURA_URI = get_parameter("HASURA_URI_PROD")
    HASURA_ADMIN_SECRET = get_secret("HASURA_ADMIN_SECRET")
    HASURA_HEADERS = { "Content-Type": "application/json", "x-hasura-admin-secret": HASURA_ADMIN_SECRET }
    success = True
    google_drive_id = ""

    query = f"""
        {{
        projects_by_pk(id: {project_id}) {{
            id
            google_drive_id
        }}
        }}
    """

    try:
        r = requests.post(HASURA_URI, json = {'query' : query}, headers = HASURA_HEADERS)

        if r.status_code != 200:
            error_list.append(r.text)
            print(r.text)
            success = False
        else:
            google_drive_id = json.loads(r.text)['data']['projects_by_pk']['google_drive_id']
            print(r.text)

    except Exception as e:
        error_list.append(str(e))
        print(str(e))
        success = False

    return google_drive_id if success else success

def get_email(staff_id):
    HASURA_URI = get_parameter("HASURA_URI_PROD")
    HASURA_ADMIN_SECRET = get_secret("HASURA_ADMIN_SECRET")
    HASURA_HEADERS = { "Content-Type": "application/json", "x-hasura-admin-secret": HASURA_ADMIN_SECRET }
    success = True
    email = ""

    query = f"""
    {{
        staffs_by_pk(id: {staff_id}) {{
            email
        }}
    }}
    """
    try:
        r = requests.post(HASURA_URI, json = {'query' : query}, headers = HASURA_HEADERS)

        if r.status_code != 200:
            error_list.append(r.text)
            print(r.text)
            success = False
        else:
            email = json.loads(r.text)['data']['staffs_by_pk']['email']
            print(r.text)

    except Exception as e:
        error_list.append(str(e))
        print(str(e))
        success = False

    return email if success else success

def lambda_handler(event, context):
    print("event:", event)
    result = {}
    statusCode = 500
    google_drive_id = ""
    email = ""

    project_id = json.loads(event['body'])['event']['data']['old']['project_id']
    staff_id = json.loads(event['body'])['event']['data']['old']['staff_id']
    google_drive_id = get_google_drive_id(project_id)
    email = get_email(staff_id)

    try:
        if email == "" or google_drive_id == "" or not remove_permission(email, google_drive_id):
            statusCode = 400
            result['status'] = "error"
            result['message'] = f"Failed to remove permissions for staff id {staff_id}"
            result['error'] = str(error_list)
        else:
            statusCode = 200
            result['status'] = "success"
            result['message'] = f"Successfully removed staff id {staff_id} permissions for project id {project_id}'s google drive folder"

    except Exception as e:
        statusCode = 400
        result['status'] = "error"
        result['message'] = f"Failed to remove permissions for staff id {staff_id}"
        result['error'] = str(e)

    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(result)
    }
