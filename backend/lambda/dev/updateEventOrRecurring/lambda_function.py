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
    
    # Single event --> Recurring event
    if ('id' in eventsOrRecurring['recurringData'] and eventsOrRecurring['recurringData']['id'] is None) and eventsOrRecurring['recurringData']['frequency'] != 'None':
        r = eventsOrRecurring['recurringData']
        eventsOrRecurring['start_date'] = r.pop("start_date",eventsOrRecurring.pop("date", None))
        r.pop("id", None)
        r.pop("name", None)
        r.pop("note", None)
        r.pop("start_time", None)
        r.pop("end_time", None)
        r.pop("pwas", None)
        r.pop("volunteers", None)
        r.pop("is_all", None)
        eventsOrRecurring = {**eventsOrRecurring,**eventsOrRecurring['recurringData']}
        if eventsOrRecurring['end_date'] == "":
            eventsOrRecurring["end_date"] = None
        del eventsOrRecurring['recurringData']

        query = f"""
        mutation eventToRecurring ($recurring: recurring_insert_input!){{
            delete_events_by_pk(id: {eventsOrRecurring.pop("id", 0)}) {{
                id
            }}
            
            insert_recurring_one(object: $recurring) {{
                id
            }}
        }}
        """
        data = {"recurring": eventsOrRecurring}
        
    # Recurring event --> Single event
    elif ('id' in eventsOrRecurring['recurringData'] and eventsOrRecurring['recurringData']['id'] is not None) and eventsOrRecurring['recurringData']['frequency'] == 'None':
        eventsOrRecurring.pop('id', None)
        r = eventsOrRecurring.pop("recurringData", None)
        query = f"""
        mutation RecurringToSingle ($event: events_insert_input!) {{
        delete_recurring_by_pk(id: {r.pop("id",0)}) {{
            id
        }}
        insert_events_one (object: $event) {{
            id
        }}
        }}
        """
        data = {'event': eventsOrRecurring}
    # Adding to event only
    elif eventsOrRecurring["recurringData"]["frequency"] == "None":
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
    elif eventsOrRecurring['recurringData']['is_all'] == 2:
        recurring = eventsOrRecurring["recurringData"]
        id = recurring.pop("id", None)
        recurring.pop("is_all", None)
        pwas = []
        vols = []
        proj_id = eventsOrRecurring['project_id']
        if recurring['end_date'] == "":
            recurring["end_date"] = None

        for num in recurring['pwas']:
            pwa = {"pwa_id": num, "project_id": proj_id, "recurring_id": id}
            pwas.append(pwa)
        recurring['pwas'] = pwas
        for ch in recurring['volunteers']:
            vol = {"vol_id": ch, "project_id": proj_id, "recurring_id": id}
            vols.append(vol)
        recurring['volunteers'] = vols

        query = f"""
                mutation UpdateAllEvents($id: Int!, $recurring: recurring_set_input!, $pwas: [recurring_pwas_insert_input!]!, $vols: [recurring_vols_insert_input!]!) {{
                    update_recurring_by_pk(pk_columns: {{id: $id}}, _set: $recurring) {{
                        id
                    }}

                    delete_recurring_pwas(where: {{
                        _and: [{{recurring_id: {{_eq: $id}}}}]
                    }}) {{
                        affected_rows
                    }}

                    insert_recurring_pwas(objects: $pwas) {{
                        affected_rows
                    }}

                    delete_recurring_vols(where: {{
                        _and: [{{recurring_id: {{_eq: $id}}}}]
                    }}) {{
                        affected_rows
                    }}

                    insert_recurring_vols(objects: $vols) {{
                        affected_rows
                    }}
                }}
              """
        data = {
            "id": id,
            "pwas": recurring.pop("pwas", []),
            "vols": recurring.pop("volunteers", []),
            "recurring": recurring
        }
    # Adding to this and future events
    elif eventsOrRecurring['recurringData']['is_all'] == 1:
        recurring = eventsOrRecurring['recurringData']
        if recurring['end_date'] == "":
            recurring["end_date"] = None
        data = {'recurring': eventsOrRecurring}
        recurring_id = recurring.pop("id", None)
        event_date = eventsOrRecurring['date']
        recurring.pop("is_all", None)
        recurring['project_id'] = eventsOrRecurring['project_id']

        for i in range(len(recurring['volunteers'])):
            vol = recurring['volunteers'][i]
            recurring['volunteers'][i] = {"vol_id": vol}
        for i in range(len(recurring['pwas'])):
            pwa = recurring['pwas'][i]
            recurring['pwas'][i] = {"pwa_id": pwa}

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
        recurring['pwas'] = {"data": recurring["pwas"]}
        recurring['volunteers'] = {"data": recurring["volunteers"]}
        data = {"recurring": recurring}
    # Adds to a single event with recurring
    else:
        recurr = eventsOrRecurring.pop("recurringData", None)
        recurr_id = recurr.pop("id", None)
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
