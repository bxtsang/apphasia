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

# Generate notifications to staffs with the message given
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
    query = """
    mutation ($notifs: [notifications_insert_input!]!) {
      insert_notifications(objects: $notifs) {
        affected_rows
      }
    }
    """
    response = execute_query_with_variables(query,{"notifs": data})

# Send archive message to all staffs
def send_all_staffs(name, table, entity_id):
    message = f"{name} has been archived."
    query = """
    {
      staffs {
        id
      }
    }
    """
    staffs = execute_query(query)['data']['staffs']
    generate_notification(staffs, message, table, entity_id)

# Pre process existing objects of PWAs & Volunteers
def pre_process_old(old,table):
    for k in old:
        if table == "volunteers" and k in ["project","ic"]:
            old.pop(k)
            break
        elif table == "pwas" and k == "project":
            proj = old.pop(k)
            old["project_id"] = proj['id']
            break
        if type(old[k]) is list:
            for ch in old[k]:
                pre_process_old(ch,table)
    return old
# Pre process new objects of PWAs & Volunteers
def pre_process_new(new):
    for k in new:
        if type(new[k]) is dict:
            if "data" in new[k]:
                new[k] = new[k]['data']
                if type(new[k]) is list:
                    for ch in new[k]:
                        pre_process_new(ch)
                else:
                    pre_process_new(new[k])
    return new

# Get list of the fields that were updated
def get_updated_fields(new,old):
    result = []
    for key in old:
        if key not in new:
            result.append(key)
            continue
        if type(old[key]) is dict:
            result += get_updated_fields(new[key], old[key])
        else:
            if old[key] != new[key]:
                result.append(key)
    return result

# Pre process list of updated fields to make them look pretty for the message
def change_details(updated):
    result = []
    change = {
        "contact_num": "Contact Number",
        "project_vols": "Projects",
        "vol_languages": "Languages",
        "vol_voltypes": "Voltypes",
        "comm_mode": "Mode of Communication",
        "comm_diff": "Communication Difficulties",
        "nok": "NOK",
        "ws_place": "Work/Study location",
        "is_active": "Archive Status",
        "is_speech_therapist": "Speech Therapist",
        "pwas": "PWAs",
        "vols": "Volunteers",
        "owner_id": "Owner",
        "dob": "DOB"
    }
    for ch in updated:
        if ch in change:
            ch = change[ch]
        else:
            ch = " ".join(ch.split("_")).title()
        result.append(ch)
    return result

# Pre process existing objects of Staffs & Projects
def pre_process_staff_project(old):
    temp = {}
    if "role_description" in old:
        role = old.pop("role_description")
        old["role"] = role["role"]
    if "owner" in old:
        old["owner_id"] = old["owner"]['id']
    for k in old.keys():
        if type(old[k]) is not list:
            temp[k] = old[k]
    
    return temp
        
# Get list of the fields that were updated in Staffs and Projects
def get_staff_project_updated_details(old, new):
    result = []
    if "staff_id" in new:
        new['id'] = new.pop("staff_id")
    for k in new:
        if type(new[k]) is list:
            if new[k]:
                add = k.split("_")[0]
                if add not in result:
                    result.append(add)
        elif type(new[k]) is dict:
            result += get_staff_project_updated_details(old, new[k])
        elif k not in old or new[k] != old[k]:
            result.append(k)
    return change_details(result)

def lambda_handler(event, context):
    result = {}
    statusCode = 200

    try:
        event_body = json.loads(event['body'])
        staff_id = event_body['session_variables']['x-hasura-user-id'] if 'x-hasura-user-id' in event_body['session_variables'] else None 
        updateData = event_body['input']['updateNotificationData']
        old = updateData['old']
        new = updateData['new']

        # Get table of entity
        if "role_description" in old:
            table = "staffs"
        elif "rejected_date" in old:
            table = "volunteers"
        elif "owner" in old:
            table = "projects"
        else:
            table = "pwas"
            
        # Get id of entity
        entity_id = new["id"] if "id" in new else new["staff_id"]
        
        # Get message if entity is pwas/volunteers
        if table in ["pwas","volunteers"]:
            old = pre_process_old(old,table)
            new = pre_process_new(new)
            if "general_info" in updateData:
                new["general_info"] = updateData["general_info"]
            
            # Get name/title of entity
            name = new["general_info"]["name"]
                
            
            updated = change_details(get_updated_fields(new,old))
            message = f"{', '.join(updated)} of {name} has been updated."
            
            # Archive notifications
            if "Archive Status" in updated and not new["is_active"]:
                if table == "pwas":
                    # Notify when pwa is archived
                    name = "PWA " + name
                    send_all_staffs(name,table,entity_id)
                    
                    # Notify befriender they will be removed
                    message = f"Your {name} that is attached to you will be removed in 30 days."
                    data = {"peep": entity_id}
                    query = """
                    query ($peep: Int!) {
                      project_pwa_staffs(where: {_and: {pwa_id: {_eq: $peep}, project: {title: {_eq: "Befrienders"}}}}) {
                        staff_id
                      }
                    }
                    """
                    staffs = execute_query_with_variables(query,data)['data']['project_pwa_staffs']
                    generate_notification(staffs, message, table, entity_id)
                    
                    # Notify PWA in project that they will be removed
                    data = {"peep": entity_id}
                    query = """
                    query ($peep: Int!) {
                      project_pwa(where: {_and: {project: {title: {_neq: "Befrienders"}}, pwa_id: {_eq: $peep}}}) {
                        project {
                          id
                          owner_id
                          title
                        }
                      }
                    }
                    """
                    staffs = execute_query_with_variables(query,data)['data']['project_pwa']
                    for staff in staffs:
                        project = staff.pop("project")
                        sendee = [{"id": project['owner_id']}]
                        project_id = project['id']
                        message = f"{name} will be removed from {project['title']} in 30 days."
                        generate_notification(sendee, message, table, project_id)
                elif table == "volunteers":
                    # Notify when vol is archived
                    name = "Volunteer " + name
                    send_all_staffs(name,table,entity_id)
                    
                    # Notify vol in project that they will be removed
                    data = {"peep": entity_id}
                    query = """
                    query ($peep: Int!) {
                      project_vol(where: {vol_id: {_eq: $peep}}) {
                        project {
                          id
                          owner_id
                          title
                        }
                      }
                    }
                    """
                    staffs = execute_query_with_variables(query,data)['data']['project_vol']
                    for staff in staffs:
                        project = staff.pop("project")
                        sendee = [{"id": project['owner_id']}]
                        project_id = project['id']
                        message = f"{name} will be removed from {project['title']} in 30 days."
                        generate_notification(sendee, message, table, project_id)

        if table == "staffs":
            
            # Pre process & craft message
            old = pre_process_staff_project(old)
            updated = get_staff_project_updated_details(old, new)
            name = new["name"]
            message = f"{', '.join(updated)} of {name} has been updated."
            
            # Archive notifications
            if "Archive Status" in updated and not new["is_active"]:
                send_all_staffs(name,table,entity_id)
                
                # Notify for projects where staff was the IC
                query = """
                query ($staff: Int!) {
                  projects(where: {owner_id: {_eq: $staff}}) {
                    id
                    title
                  }
                }
                """
                data = {"staff": entity_id}
                projects = execute_query_with_variables(query,data)['data']['projects']
                table = "projects"
                for project in projects:
                    title = project.pop("title")
                    message = f"Project {title} will not have an IC once {name} is removed in 30 days."
                    generate_notification(staffs, message, table, project['id'])
                
                # Notify for projects where staff was in it
                data = {"staff": entity_id}
                query = """
                query ($staff: Int!) {
                  project_staffs(where: {staff_id: {_eq: $staff}}) {
                    project {
                      owner_id
                      title
                      id
                    }
                  }
                }
                """
                staffs = execute_query_with_variables(query,data)['data']['project_staffs']
                for staff in staffs:
                    project = staff.pop("project")
                    sendee = [{"id": project['owner_id']}]
                    project_id = project['id']
                    message = f"{name} will be removed from {project['title']} in 30 days."
                    generate_notification(sendee, message, table, project_id)
        
            # Only send notifications if staff is not part of the core team
            if new['role'] in ["core_volunteer", "intern"]:
                data = {"staff": entity_id}
                query = """
                query ($staff: Int!) {
                  staff_supervisors(where: {staff_id: {_eq: $staff}}) {
                    supervisor_id
                  }
                  project_staffs(where: {staff_id: {_eq: $staff}}) {
                    project {
                      owner_id
                      title
                      id
                    }
                  }
                }
                """
                # Notify for Project IC where staff was in it
                response = execute_query_with_variables(query,data)['data']
                staffs = response['project_staffs']
                sendees = []
                for staff in staffs:
                    project = staff.pop("project")
                    sendee = project['owner_id']
                    if sendee not in sendees:
                        sendees.append(sendee)
                
                # Notify Supervisors
                staffs = response['staff_supervisors']
                for staff in staffs:
                    sendee = staff['supervisor_id']
                    if sendee not in sendees:
                        sendees.append(sendee)

                sendees = [{"id": sendee} for sendee in sendees]
                generate_notification(sendees, message, table, entity_id, "UPDATE")
                
                # Notify staff if changes were not made by them
                if entity_id != staff_id and staff_id:
                    data = {"staff": staff_id}
                    query = """
                    query ($staff: Int!) {
                      staffs_by_pk(id: $staff){
                        name
                      }
                    }
                    """
                    name = execute_query_with_variables(query,data)['data']['staffs_by_pk']['name']
                    sendee = [{'id': entity_id}]
                    message = f"{', '.join(updated)} of your profile has been updated by {name}."
                    generate_notification(sendee, message, table, entity_id, "UPDATE")
                    
                
        elif table == "pwas":
            # Notify befrienders attached to PWA
            data = {"peep": entity_id}
            query = """
            query ($peep: Int!) {
              project_pwa_staffs(where: {_and: {pwa_id: {_eq: $peep}, project: {title: {_eq: "Befrienders"}}}}) {
                staff_id
              }
            }
            """
            staffs = execute_query_with_variables(query,data)['data']['project_pwa_staffs']
            generate_notification(staffs, message, table, entity_id,"UPDATE")
        elif table == "volunteers":
            # Notify vol supervisor
            staffs = old["vol_ic"]
            generate_notification(staffs, message, table, entity_id,"UPDATE")
        elif table == "projects":
            old = pre_process_staff_project(old)
            updated = get_staff_project_updated_details(old, new)
            
            
            owner = old["owner_id"]
            title = old["title"]
            # Notify change of project owner
            if "Owner" in updated:
                updated.remove("Owner")
                data = {"staff": new["project"]["owner_id"]}
                query = """
                query ($staff: Int!) {
                  staffs_by_pk(id: $staff){
                    name
                  }
                }
                """
                name = execute_query_with_variables(query,data)['data']['staffs_by_pk']['name']
                message = f"{title} has changed IC to {name}."
                query = """
                {
                  staffs {
                    id
                  }
                }
                """
                staffs = execute_query(query)['data']['staffs']
                generate_notification(staffs, message, table, entity_id, "UPDATE")
                
            # Notify project IC of new project details updated
            if entity_id != staff_id:
                if staff_id:
                    data = {"staff": staff_id}
                    query = """
                    query ($staff: Int!) {
                      staffs_by_pk(id: $staff){
                        name
                      }
                    }
                    """
                    name = execute_query_with_variables(query,data)['data']['staffs_by_pk']['name']
                else:
                    name = "admin"
                sendee = [{'id': old["owner_id"]}]
                message = f"{', '.join(updated)} of {title} has been updated by {name}."
                generate_notification(sendee, message, table, entity_id, "UPDATE")

        result['status'] = "Success"
        result['message'] = "Successfully added notifications."
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
