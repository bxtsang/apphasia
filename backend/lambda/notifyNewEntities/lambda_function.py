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

def generate_notification(staffs, message, table, entity_id, exclude=[], operation="INSERT"):
    data = []
    for staff in staffs:
        the_id = staff['id'] if 'id' in staff else staff['staff_id']
        if the_id in exclude:
            continue
        sendee = {
            "staff_id": the_id,
            "message": message,
            "type": table,
            "entity_id": entity_id,
            "operation": operation
        }
        data.append(sendee)

    # Send notifs to staffs
    query = """
    mutation ($notifs: [notifications_insert_input!]!) {
      insert_notifications(objects: $notifs) {
        affected_rows
      }
    }
    """
    response = execute_query_with_variables(query,{"notifs": data})

def send_all_staffs(message, table, entity_id, exclude=[]):
    query = """
    {
      staffs {
        id
      }
    }
    """
    staffs = execute_query(query)['data']['staffs']
    generate_notification(staffs, message, table, entity_id, exclude)

def lambda_handler(event, context):
    result = {}
    statusCode = 200

    try:
        event_body = json.loads(event['body'])
        insertData = event_body['input']['insertNotificationsData']
        staff_id = event_body['session_variables']['x-hasura-user-id'] if 'x-hasura-user-id' in event_body['session_variables'] else None
        table = insertData['table']
        identifier = insertData['entity_id']

        entities = {
            "pwas": ["people_external","name",""],
            "volunteers": ["people_external","name",""],
            "staffs": ["staffs","name","role"],
            "projects": ["projects","title","owner_id"]
        }

        # Get details of entity
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

        if table == "staffs":
            # Send notification to all staff
            role = " ".join(entity['role'].split("_")).title()
            message = f"A new {role} has been added."
            send_all_staffs(message,table,identifier,[identifier,staff_id])

            # Send notification to supervisor
            message = f"You have been tagged as a supervisor to {entity['name']}."
            data = {"staff": identifier}
            query = """
            query ($staff: Int!) {
                  staff_supervisors(where: {staff_id: {_eq: $staff}}) {
                    supervisor_id
                  }
            }
            """
            staffs = execute_query_with_variables(query,data)['data']['staff_supervisors']
            sendees = [{"id": staff['supervisor_id']} for staff in staffs]
            generate_notification(sendees, message, table, identifier, [staff_id])
        elif table == "pwas":
            # Send notification to all staff
            message = "A new PWA has been added."
            send_all_staffs(message,table,identifier,[staff_id])

        elif table == "volunteers":
            # Send notification to all staff
            message = "A new Volunteer has been added."
            send_all_staffs(message,table,identifier,[staff_id])

        elif table == "projects":

            # Send notification to core team
            message = "A new Project has been added."
            data = {"project": identifier}
            query = """
            query ($project: Int!) {
              staffs(where: {role: {_eq: core_team}}) {
                id
              }
              projects_by_pk(id: $project) {
                owner_id
                title
              }
            }
            """
            response = execute_query_with_variables(query,data)['data']
            generate_notification(response['staffs'], message, table, identifier, [staff_id])

            # Send notification to new project owner
            owner_id = response['projects_by_pk']['owner_id']
            if owner_id != staff_id and not staff_id:
                message = f"You've been assigned to {response['projects_by_pk']['title']} as project IC"
                generate_notification([{"id": owner_id}], message, table, identifier)
        result['status'] = "Success"
        result['message'] = "Successfully added notifications"
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
