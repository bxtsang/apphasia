import json
import requests
import os
import boto3

def get_secret():
    secret_name = "HASURA_ADMIN_SECRET"

    response = clientSecret.get_secret_value(
        SecretId = secret_name
    )

    return json.loads(response['SecretString'])['HASURA_ADMIN_SECRET']

# ENV VARIABLES
clientSecret = boto3.client('secretsmanager')
HASURA_URI = os.environ['HASURA_URI']
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
            print(response['errors'][0]['message'])

        print(response)
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
            print(response['errors'][0]['message'])

        # print(response)
        return  response

    except Exception as e:
        print(e)
        success = False
        return "error occurred"

def generate_notification(staffs, message, table, entity_id, operation="DELETE"):
    data = []
    for staff in staffs:
        the_id = staff['id'] if 'id' in staff else staff['staff_id']
        sendee = {
            "staff_id": the_id, 
            "message": message, 
            "type": table, 
            "entity_id": entity_id, 
            "operation": operation
        }
        data.append(sendee)

    # Send notifs to staffs
    print(data)
    query = """
    mutation ($notifs: [notifications_insert_input!]!) {
      insert_notifications(objects: $notifs) {
        affected_rows
      }
    }
    """
    response = execute_query_with_variables(query,{"notifs": data})

def lambda_handler(event, context):
    result = {}
    statusCode = 200

    try:
        event_body = json.loads(event['body'])
        insertData = event_body['input']['insertNotificationsData']
        table = insertData['table']
        identifier = insertData['entity_id']
        entities = {
            "pwas": ["people_external","name",""], 
            "volunteers": ["people_external","name",""], 
            "staffs": ["staffs","name","role"],
            "projects": ["projects","title","owner_id"]
        }

        data = {"identifier": identifier}
        query = f"""
        query ($identifier: Int!) {{
          {entities[table][0]}_by_pk(id: $identifier){{
            {entities[table][1]}
            {entities[table][2]}
          }}
        }}
        """
        entity = execute_query_with_variables(query,data)["data"][f"{entities[table][0]}_by_pk"]        

        result['status'] = "Success"
        result['message'] = entity
    except Exception as e:
        raise e
        result['status'] = "Internal Error"
        result['message'] = "An error occurred, see CloudWatch for more information"
    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(result)
    }
