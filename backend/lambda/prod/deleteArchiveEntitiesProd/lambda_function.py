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
        entities = ["volunteers", "projects", "pwas", "staffs", "rejected volunteers"]

        for entity in entities:
            returning = "id"
            if entity == "staffs":
                returning += ", email"

            sql = f"DELETE FROM {entity} WHERE is_active = FALSE AND EXTRACT(DAY FROM (current_date at time zone '+08') - updated_at) >= 0 RETURNING {returning};"
            if entity == "rejected volunteers":
                sql = f"DELETE FROM volunteers WHERE rejected_date IS NOT NULL AND status ='Rejected' AND EXTRACT(DAY FROM (current_date at time zone '+08') - rejected_date) >= 30 RETURNING id;"

            query = {
                "type": "run_sql",
                "args": {
                    "sql": sql
                }
            }
            response = execute_query(query, True)

            # Error occurred
            if "result" not in response:
                result[entity] = json.dumps(response)
                continue

            res_ids = response['result']
            result[entity] = res_ids
            print(entity,res_ids)

            if len(res_ids) <= 1:
                result[entity] = f"No {entity}(s) to remove."
                continue

            message = ", ".join([e_id[0] for e_id in res_ids[1:]])
            result[entity] = f" {entity} id(s) {message} has/have been removed."
            # Remove staffs from AWS Cognito
            if entity == "staffs":
                message = ""
                for staff in res_ids[1:]:
                    try:
                        response = client.admin_delete_user(
                            UserPoolId=get_parameter("USER_POOL_ID"),
                            Username=staff[1]
                        )
                        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                            print(response)
                            success = False
                        message += str(staff[0]) + ", "
                
                    except Exception as e:
                        print(e)
                message = message[:-2]
                result[entity] = f" staff id(s) {message} has/have been removed."

            # Remove pwa/vol from people_external table
            if entity in ["pwas", "volunteers", "rejected volunteers"]:
                people = f"({message})"
                sql = f"DELETE FROM people_external WHERE id IN {people} RETURNING id;"
                query = {
                    "type": "run_sql",
                    "args": {
                        "sql": sql
                    }
                }
                response = execute_query(query, True)
                if "result" not in response:
                    result[entity] = json.dumps(response)

        statusCode = 200
        result['status'] = 'success'

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