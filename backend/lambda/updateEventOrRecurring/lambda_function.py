import boto3
import json
import os
import requests

client = boto3.client('cognito-idp')
clientSecret = boto3.client('secretsmanager')
hasura_url = os.environ['HASURA_URI']

def lambda_handler(event, context):
    result = {}
    statusCode = 500
    eventsOrRecurring = json.loads(event['body'])['input']['updateEventData']
    hasura_secret = get_secret()

    headers = {
            "Content-Type": "application/json",
            "x-hasura-admin-secret": hasura_secret
        }

    # Adding to event only
    if eventsOrRecurring["recurringData"]["frequency"] == "None":
        eventsOrRecurring.pop("recurringData", None)
        event_id = eventsOrRecurring.pop("id", None)
        query = f"""
        mutation updateSingleEvent($event: events_insert_input!) {{
            delete_events_by_pk(id: {event_id}) {{
                id
            }}
            insert_events_one(object: $event) {{
                id
            }}
        }}
        """
        data = {"event": eventsOrRecurring}

    # Adding to all events
    elif eventsOrRecurring['recurringData']['is_all']:
        recurring = eventsOrRecurring["recurringData"]
        id = recurring.pop("id", None)
        recurring.pop("is_all", None)
        recurring.pop("pwas", None)
        recurring.pop("vols", None)
        if recurring['end_date'] == "":
            recurring["end_date"] = None
        for ch in recurring['pwas_to_add']:
            ch['project_id'] = eventsOrRecurring['project_id']
            ch['recurring_id'] = id
        for ch in recurring['vols_to_add']:
            ch['project_id'] = eventsOrRecurring['project_id']
            ch['recurring_id'] = id
        query = f"""
        mutation UpdateAllEvents($id: Int!, $recurring: recurring_set_input!, $pwas_to_add: [recurring_pwas_insert_input!]!, $pwas_to_remove: [Int!], $vols_to_add: [recurring_vols_insert_input!]!, $vols_to_remove: [Int!]) {{
            update_recurring_by_pk(pk_columns: {{id: $id}}, _set: $recurring) {{
                id
            }}

            insert_recurring_pwas(objects: $pwas_to_add) {{
                affected_rows
            }}
            
            delete_recurring_pwas(where: {{
                _and: [{{
                pwa_id: {{_in: $pwas_to_remove}},
                recurring_id: {{_eq: $id}}
                }}]
            }}) {{
                affected_rows
            }}

            insert_recurring_vols(objects: $vols_to_add) {{
                affected_rows
            }}
            
            delete_recurring_vols(where: {{
                _and: [{{
                vol_id: {{_in: $vols_to_remove}},
                recurring_id: {{_eq: $id}}
                }}]
            }}) {{
                affected_rows
            }}
        }}
              """
        data = {
            "id": id,
            "pwas_to_add": recurring.pop("pwas_to_add", []),
            "pwas_to_remove": recurring.pop("pwas_to_remove", []),
            "vols_to_add": recurring.pop("vols_to_add", []),
            "vols_to_remove": recurring.pop("vols_to_remove", []),
            "recurring": recurring
        }
        
    # Adding to this and future events
    else:
        recurring = eventsOrRecurring['recurringData']
        if recurring['end_date'] == "":
            recurring["end_date"] = None
        data = {'recurring': eventsOrRecurring}
        recurring_id = recurring.pop("id", None)
        event_date = eventsOrRecurring['date']
        recurring.pop("is_all", None)
        recurring['project_id'] = eventsOrRecurring['project_id']
        for num in recurring['volunteers']:
            if num not in recurring['vols_to_remove']:
                recurring['vols_to_add'].append({"vol_id": num})
        for num in recurring['pwas']:
            if num not in recurring['pwas_to_remove']:
                recurring['pwas_to_add'].append({"pwa_id": num})
        recurring.pop("pwas_to_remove", None)
        recurring.pop("vols_to_remove", None)
        query = f"""
        mutation UpdateThisAndFutureEvent($recurring: recurring_insert_input!) {{
            update_recurring_by_pk(pk_columns: 	{{id: {recurring_id}}}, _set: {{end_date: "{event_date}"}}) {{
            id
            }}
            
            insert_recurring_one(object: $recurring) {{
            id
            }}
        }}
        """
        recurring['pwas'] = {"data": recurring.pop("pwas_to_add", [])}
        recurring['volunteers'] = {"data": recurring.pop("vols_to_add", [])}
        data = {"recurring": recurring}
    try:
        print(json.dumps(data))
        r = requests.post(hasura_url, json={'query': query, "variables": data}, headers=headers)
        print(r.status_code)
        print(r.text)
        json_response = json.loads(r.text)
        if "errors" not in json_response and "error" not in json_response:
            statusCode = 200
            result['status'] = "sent"
            result['message'] = "query successfully sent to hasura"
        else:
            statusCode = 400
            result['code'] = str(r.status_code)
            result['message'] = r.text
    except Exception as e:
        statusCode = 400
        result['code'] = str(r.status_code)
        result['message'] = r.text

    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(result)
    }



def get_secret():
    secret_name = "HASURA_ADMIN_SECRET"

    response = clientSecret.get_secret_value(
        SecretId = secret_name
    )


    return json.loads(response['SecretString'])['HASURA_ADMIN_SECRET']
