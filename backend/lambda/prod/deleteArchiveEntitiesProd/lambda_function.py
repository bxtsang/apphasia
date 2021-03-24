import requests
import os
import json
import boto3

def get_parameter(parameter):
    response = client_ssm.get_parameter(
    Name=parameter,
    WithDecryption=False
    )

    return response['Parameter']['Value']

def get_secret():
    secret_name = "HASURA_ADMIN_SECRET"

    response = clientSecret.get_secret_value(
        SecretId = secret_name
    )

    return json.loads(response['SecretString'])['HASURA_ADMIN_SECRET']

# ENV VARIABLES
client = boto3.client('cognito-idp')
clientSecret = boto3.client('secretsmanager')
client_ssm = boto3.client('ssm')
HASURA_URI = get_parameter("HASURA_URI_PROD")
HASURA_URI_SQL = HASURA_URI[:-7] + "query"
HASURA_ADMIN_SECRET = get_secret()
HASURA_HEADERS = { "Content-Type": "application/json", "x-hasura-admin-secret": HASURA_ADMIN_SECRET }

def execute_query_with_variables(query, data, sql=False):
    success = True
    try:
        r = requests.post(HASURA_URI_SQL if sql else HASURA_URI, json = {'query' : query, 'variables': data}, headers = HASURA_HEADERS)

        response = json.loads(r.text)
        if r.status_code != 200 or "errors" in response:
            success = False

        return response

    except Exception as e:
        print(e)
        success = False
        return e.message

def execute_query(query, sql=False):
    success = True
    try:
        if sql:
            r = requests.post(HASURA_URI_SQL, json = query, headers = HASURA_HEADERS)
        else:
            r = requests.post(HASURA_URI, json = {'query' : query}, headers = HASURA_HEADERS)

        response = json.loads(r.text)
        if r.status_code != 200 or "errors" in response:
            success = False

        return  response

    except Exception as e:
        print(e)
        success = False
        return "error occurred"

def lambda_handler(event, context):
    result = {}
    statusCode = 500

    try :
        secret = get_secret()
        query = {
            "type": "run_sql",
            "args": {
                "sql": """
                DELETE FROM volunteers WHERE rejected_date IS NOT NULL AND status ='Rejected' AND EXTRACT(DAY FROM (current_date at time zone 'UTC') - rejected_date) >= 30;
                DELETE FROM volunteers WHERE is_active = FALSE AND EXTRACT(DAY FROM (current_date at time zone 'UTC') - updated_at) >= 30;
                DELETE FROM projects WHERE is_active = FALSE AND EXTRACT(DAY FROM (current_date at time zone 'UTC') - updated_at) >= 30;
                DELETE FROM pwas WHERE is_active = FALSE AND EXTRACT(DAY FROM (current_date at time zone 'UTC') - updated_at) >= 30;
                DELETE FROM staffs WHERE is_active = FALSE AND EXTRACT(DAY FROM (current_date at time zone 'UTC') - updated_at) >= 30 RETURNING email;"""
            }
        }

        response = execute_query(query, True)
        staffs = response['result']
        if len(staffs) > 1:
            for staff in staffs[1:]:
                try:
                    response = client.admin_delete_user(
                        UserPoolId=get_parameter("USER_POOL_ID"),
                        Username=staff[0]
                    )
                    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                        print(response)
                        success = False
                
            
                except Exception as e:
                    print(e)
        statusCode = 200
        result['status'] = 'success'
        result['message'] = str(staffs)

    except Exception as e:
        print(e)
        statusCode = 400
        result['status'] = "failed"
        result['message'] = str(e)

    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(result)
    }