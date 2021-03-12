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
hasura_url = os.environ['HASURA_URI']
hasura_admin_secret = get_secret()

def insert_people(headers, table):
    query = f"""
            {{
                staffs {{
                id
                }}
            }}
    """
    try:
        # Query for list of staffs
        r = requests.post(hasura_url, json={'query': query}, headers=headers)
        json_response = json.loads(r.text)

        if "errors" not in json_response:
            staffs = json_response['data']["staffs"]
            data = []
            for staff in staffs:
                row = {"staff_id": staff['id'], "message": f"A new {table[:-1]} has joined"}
                data.append(row)
        else:
            statusCode = 400
            result['code'] = str(r.status_code)
            result['message'] = r.text
            return {
                'statusCode': 400,
                "body": json.dumps(json_response)
            }
        # Send notifs to staffs
        query = """
        mutation ($notifs: [notifications_insert_input!]!) {
          insert_notifications(objects: $notifs) {
            affected_rows
          }
        }
        """
        r = requests.post(hasura_url, json={'query': query, "variables": {"notifs": data}}, headers=headers)
        
        return {
            'statusCode': 200,
            'body': "Notifications successfully created"
        }
    except Exception as e:
        raise e
        return {
            'statusCode': 500,
            "body": "An error occurred when creating notifications."
        }

# def insert_staff_supervisor(headers, table):
    
def lambda_handler(event, context):
    event = json.loads(event['body'])
    table = event['table']['name']
    # Operation on table | INSERT, UPDATE, DELETE, MANUAL
    op = event['event']['op']
    print(event)
    headers = { 
        "Content-Type": "application/json",
        "x-hasura-admin-secret": hasura_admin_secret
    }
    
    # INSERT OPERATION
    if op == "INSERT":
        if table in ["pwas","volunteers","staffs"]:
            return insert_people(headers, table)
        elif table == "staff_supervisors":
            pass
            
    # UPDATE OPERATION
    elif op == "UPDATE":
        pass
    
    # DELETE OPERATION
    elif op == "DELETE":
        pass
    
    # MANUAL OPERATIONS (FOR TESTING)
    else:
        if table in ["pwas","volunteers","staffs"]:
            return insert_people(headers, table)
        elif table == "staff_supervisors":
            pass

    return {
        'statusCode': 200,
        'body': "Notifications successfully created"
    }
