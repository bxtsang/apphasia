import json
import os
from Google import Create_Service

CLIENT_SECRET_FILE = "credentials.json"
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def lambda_handler():
    # print(event)
    result = {}
    statusCode = 500

    params = {
            'fileId': "1eWcdfPgagDGqndrAAkDymbfmTjR2k6CU"
        }

    try:
        SERVICE.files.delete(parameters = params)
        result['status'] = "success"
        result['message'] = "folder created successfully!"
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

lambda_handler()