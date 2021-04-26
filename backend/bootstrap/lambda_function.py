import json
import os
import requests
import random
from pandas import *

# Set production to true/false for production
production = True
# hasura credentials
HASURA_URI = "https://aphasia-hasura-dev.herokuapp.com/v1/graphql"
HASURA_URI_SQL = "https://aphasia-hasura-dev.herokuapp.com/v1/query"

if production:
    HASURA_URI = "https://hasura.apphasia.cf/v1/graphql"
    HASURA_URI_SQL = "https://hasura.apphasia.cf/v1/query"
HASURA_ADMIN_SECRET = "pwayismyhome12061997"
HASURA_HEADERS = { "Content-Type": "application/json", "x-hasura-admin-secret": HASURA_ADMIN_SECRET }

# api endpoints
delete_all_cognito_users = "https://83vex37vn6.execute-api.ap-southeast-1.amazonaws.com/dev"
insert_cognito_users = "https://jvuzedyfme.execute-api.ap-southeast-1.amazonaws.com/test"
create_folder_gdrive = "https://67sbpripz3.execute-api.ap-southeast-1.amazonaws.com/dev"
delete_folder_gdrive = "https://schwn3irr1.execute-api.ap-southeast-1.amazonaws.com/dev"
list_folders_gdrive = "https://hr0qbwodlg.execute-api.ap-southeast-1.amazonaws.com/dev"

# path to excel files
# Rmb to change the path to your path
path = "./"

def get_pwas():
    xls = read_excel(path + 'pwas.xls')
    pwas = xls.to_dict('records')

    for pwa in pwas:
        gen_info = {}
        gen_info["address"] = pwa.pop("address", "")
        gen_info["bio"] = pwa.pop("bio", "")
        gen_info["channel"] = pwa.pop("channel", "")
        gen_info["consent"] = pwa.pop("consent", "")
        gen_info["contact_num"] = str(pwa.pop("contact_num", ""))
        gen_info["date_joined"] = pwa.pop("date_joined", "")
        gen_info["dob"] = pwa.pop("dob", "")
        gen_info["email"] = pwa.pop("email", "")
        gen_info["gender"] = pwa.pop("gender", "")
        gen_info["notes"] = pwa.pop("notes", "")
        gen_info["name"] = pwa.pop("name", "")
        pwa['general_info'] = {"data": gen_info}

        # Languages
        languages = pwa['languages'].split(",")
        for i in range(len(languages)):
            languages[i]= {"language": languages[i].strip()}
        pwa['languages'] = {"data": languages}

        # Communication Difficulties
        dificulty = pwa['comm_diff'].split(",") if str(pwa['comm_diff']) != "nan" else []
        for i in range(len(dificulty)):
            dificulty[i]= {"difficulty": dificulty[i].strip()}
        pwa['comm_diff'] = {"data": dificulty}

        # NOK
        noks = pwa['nok'].split("|") if str(pwa['nok']) != "nan" else []
        for i in range(len(noks)):
            nok = noks[i]
            nok_details = nok.split(",")
            noks[i] = {"name": nok_details[0], "contact_num": int(nok_details[1]), "email": nok_details[2], "relationship": nok_details[3]}
        pwa['nok'] = {"data": noks}

        # if media_engagement_details is null
        if str(pwa['media_engagement_details']) == "nan":
            pwa.pop("media_engagement_details")
        # if hospital is null
        if str(pwa['hospital']) == "nan":
            pwa.pop("hospital")
        # if speech_therapist is null
        if str(pwa['speech_therapist']) == "nan":
            pwa.pop("speech_therapist")
        # if storke_date is null
        if str(pwa['stroke_date']) == "nan":
            pwa.pop("stroke_date")
        # if wheelchair is null
        if str(pwa['wheelchair']) == "nan":
            pwa.pop("wheelchair")
        # if last_contact_details is null
        if str(pwa['last_contact_details']) == "nan":
            pwa.pop("last_contact_details")
        # if notes is null
        if str(pwa['general_info']["data"]['notes']) == "nan":
            pwa['general_info']["data"].pop("notes")
        # if channel is null
        if str(pwa['general_info']["data"]['channel']) == "nan":
            pwa['general_info']["data"].pop("channel")
    return pwas

def get_staffs():
    # RMB TO CHANGE PATH OF EXCEL
    xls = read_excel(path + 'staffs.xls')
    staffs = xls.to_dict('records')
    for staff in staffs:
        languages = staff['languages'].split(",")
        staff['contact_num'] = str(staff['contact_num'])
        for i in range(len(languages)):
            languages[i]= {"language": languages[i].strip().title()}
        staff['languages'] = {"data": languages}

        supervisors = str(staff['supervisors']).split(",") if str(staff['supervisors']) != "nan" else []
        for i in range(len(supervisors)):
            supervisors[i]= {"supervisor_id": int(supervisors[i])}
        staff['supervisors'] = {"data": supervisors}

        # If nickname is null
        if str(staff['nickname']) == "nan":
            staff.pop("nickname")
        # If ws_place is null
        if str(staff['ws_place']) == "nan":
            staff.pop("ws_place")
        # If bio is null
        if str(staff['bio']) == "nan":
            staff.pop("bio")

    return staffs

def get_volunteers(staffs, randomized=True):
    # RMB TO CHANGE PATH OF EXCEL
    xls = read_excel(path + 'volunteers.xls')
    vols = xls.to_dict('records')

    for vol in vols:

        gen_info = {}
        gen_info["address"] = vol.pop("address", "")
        gen_info["bio"] = vol.pop("bio", "")
        gen_info["channel"] = vol.pop("channel", "").title()
        gen_info["consent"] = vol.pop("consent", "")
        gen_info["contact_num"] = str(vol.pop("contact_num", ""))
        gen_info["date_joined"] = vol.pop("date_joined", "")
        gen_info["dob"] = vol.pop("dob", "")
        gen_info["email"] = vol.pop("email", "")
        gen_info["gender"] = vol.pop("gender", "")
        gen_info["notes"] = vol.pop("notes", "")
        gen_info["name"] = vol.pop("name", "")
        vol['general_info'] = {"data": gen_info}
        vol['status'] = vol['status']

        # Vol IC's
        ics = []
        if randomized:
            ics = random.sample(range(1,len(staffs)),random.randrange(0,4))
            for i in range(len(ics)):
                ics[i]= {"staff_id": ics[i]}
        vol['vol_ic'] = {"data": ics}

        # Languages
        languages = vol['vol_languages'].split(",")
        for i in range(len(languages)):
            languages[i]= {"language": languages[i].strip().title()}
        vol['vol_languages'] = {"data": languages}

        # voltypes
        types = vol['vol_voltypes'].split(",") if str(vol['vol_voltypes']) != "nan" else []
        for i in range(len(types)):
            types[i]= {"voltype": types[i].strip().title()}
        vol['vol_voltypes'] = {"data": types}

        # if rejected_date is null
        if str(vol['rejected_date']) == "nan":
            vol.pop("rejected_date")
        # if status_reason is null
        if str(vol['status_reason']) == "nan":
            vol.pop("status_reason")
        # if notes is null
        if str(vol['general_info']["data"]['notes']) == "nan":
            vol['general_info']["data"].pop("notes")
        # if channel is null
        if str(vol['general_info']["data"]['channel']) == "nan":
            vol['general_info']["data"].pop("channel")
        # if nickname is null
        if str(vol['nickname']) == "nan":
            vol.pop("nickname")
        # if ws_place is null
        if str(vol['ws_place']) == "nan":
            vol.pop("ws_place")
    return vols

def get_projects(vols,staffs,pwas, randomized = True):
    # RMB TO CHANGE PATH OF EXCEL
    xls = read_excel(path + 'projects.xls')
    projects = xls.to_dict('records')
    vols_count = len(vols)
    pwas_count = len(pwas)
    staffs_count = len(staffs)

    try:
        data = {
            "parent_folder": ""
        }
        res = requests.post(list_folders_gdrive,data=json.dumps(data))

        files = json.loads(res.text)['files']

        for file in files:
            data = {"file_id": file['id']}
            res = requests.post(delete_folder_gdrive,data=json.dumps(data))

            response = json.loads(res.text)
            if res.status_code != 200 :
                print(response)

    except Exception as e:
        print(e)
        
    for project in projects:
        pwas = []
        staffs = []
        vols = []
        assign_staff = []
        assign_vol = []

        if randomized:
            # pwas
            pwas_num = random.sample(range(vols_count + 1, vols_count + pwas_count),random.randrange(1,6))
            for pwa in pwas_num:
                pwas.append({"pwa_id": pwa})
            # staffs
            staffs_num = random.sample(range(1,staffs_count),random.randrange(2,8))
            for staff in staffs_num:
                staffs.append({"staff_id": staff})
            # vols
            vols_num = random.sample(range(1,vols_count),random.randrange(1,8))
            for vol in vols_num:
                vols.append({"vol_id": vol})
            # pwa X staff X vol
            for pwa in pwas_num: 
                sample_staffs = random.sample(staffs_num, random.randrange(0,len(staffs_num)))
                for staff in sample_staffs:
                    assign_staff.append({"pwa_id": pwa, "staff_id": staff})

                sample_vols = random.sample(vols_num, random.randrange(0,len(vols_num)))
                for vol in sample_vols:
                    assign_vol.append({"pwa_id": pwa, "vol_id": vol})

        project['pwas'] = {"data": pwas}
        project['staffs'] = {"data": staffs}
        project['volunteers'] = {"data": vols}
        project['pwa_assigned_staffs'] = {"data": assign_staff}
        project['pwa_assigned_vols'] = {"data": assign_vol}

    return projects

def get_recurring(projects, randomized = True):
    xls = read_excel(path + 'recurring.xls')
    recursions = xls.to_dict('records')
    for recurr in recursions:
        if str(recurr['week']) == "nan":
            recurr.pop("week")

        if str(recurr['end_date']) == "nan":
            recurr.pop("end_date")

        if str(recurr['note']) == "nan":
            recurr.pop("note")

        pwas = []
        vols = []
        if randomized:
            # pwas & vols
            project_id = recurr['project_id']
            project = projects[project_id - 1]
            pwas_data = project['pwas']['data']
            vols_data = project['volunteers']['data']
            pwas = random.sample(pwas_data, random.randrange(0,len(pwas_data)))
            vols = random.sample(vols_data, random.randrange(0,len(vols_data)))

        recurr['pwas'] = {"data": pwas}
        recurr['volunteers'] = {"data": vols}

    return recursions

def get_events(projects, randomized = True):
    xls = read_excel(path + 'events.xls')
    events = xls.to_dict('records')
    for event in events:

        if str(event['note']) == "nan":
            event.pop("note")

        pwas = []
        vols = []
        if randomized:
            # pwas & vols
            project_id = event['project_id']
            project = projects[project_id - 1]
            pwas_data = project['pwas']['data']
            vols_data = project['volunteers']['data']
            pwas = random.sample(pwas_data, random.randrange(0,len(pwas_data)))
            vols = random.sample(vols_data, random.randrange(0,len(vols_data)))

        event['pwas'] = {"data": pwas}
        event['volunteers'] = {"data": vols}
    return events

def execute_query_with_variables(query, data, sql=False):
    success = True
    try:
        r = requests.post(HASURA_URI_SQL if sql else HASURA_URI, json = {'query' : query, 'variables': data}, headers = HASURA_HEADERS)

        response = json.loads(r.text)
        if r.status_code != 200 or "errors" in response:
            success = False
            print(response['errors'][0]['message'])

        print(response)

    except Exception as e:
        print(e)
        success = False

    print("Success!") if success else print("Error!")

def execute_query(query, sql=False):
    success = True
    try:
        if sql:
            r = requests.post(HASURA_URI_SQL, json = query, headers = HASURA_HEADERS)
        else:
            r = requests.post(HASURA_URI, json = {'query' : query}, headers = HASURA_HEADERS)

        if r.status_code != 200:
            success = False

        print(r.text)

    except Exception as e:
        print(e)
        success = False

    print("success!") if success else print("error")


def delete() :
    #--------------------DELETE--------------------
    #delete cognito users
    print("\n\n--------------------DELETING COGNITO USERS--------------------")
    try:
        success = True
        r = requests.post(delete_all_cognito_users)
        if r.status_code != 200:
            print(r.text)
            success = False
    

    except Exception as e:
        print(e)
        success = False

    print("success!") if success else print("error")
    success = True

    delete_query = "mutation {"

    #delete hasura data

    #delete projects
    delete_query += """
        delete_projects(where: {}) {
            affected_rows
        }
            """

    #delete pwas
    delete_query += """
        delete_pwas(where: {}) {
            affected_rows
        }
            """

    #delete vols
    delete_query += """
        delete_volunteers(where: {}) {
            affected_rows
        }
            """

    #delete people_external
    delete_query += """
        delete_people_external(where: {}) {
            affected_rows
        }
            """

    #delete staffs
    delete_query += """
        delete_staffs(where: {}) {
            affected_rows
        }
            """

    #delete status
    delete_query += """
        delete_status(where: {}) {
            affected_rows
        }
            """

    #delete channels
    delete_query += """
        delete_channels(where: {}) {
            affected_rows
        }
            """

    #delete recurr
    delete_query += """
        delete_recurring(where: {}) {
            affected_rows
        }
            """

    #delete events
    delete_query += """
        delete_events(where: {}) {
            affected_rows
        }
            """

    #delete pwa_contact_status
    delete_query += """
        delete_pwa_contact_status(where: {}) {
            affected_rows
        }
            """

    #delete project_task_status
    delete_query += """
        delete_project_task_status(where: {}) {
            affected_rows
        }
            """

    delete_query += "}"

    print("\n\n--------------------DELETING DATA--------------------")
    execute_query(delete_query)

def alter_sequence():
#--------------------ALTER--------------------

    #alter staffs_id_seq
    print("\n\n--------------------ALTERING SEQUENCE--------------------")
    alter_query = {
        "type": "run_sql",
        "args": {
            "sql": 'ALTER SEQUENCE staffs_id_seq RESTART 1;ALTER SEQUENCE projects_id_seq RESTART 1;ALTER SEQUENCE events_id_seq RESTART 1;ALTER SEQUENCE recurring_id_seq RESTART 1;ALTER SEQUENCE people_external_id_seq RESTART 1;ALTER SEQUENCE notifications_id_seq RESTART 1;'
        }
    }
    execute_query(alter_query, True)

def insert():
    #--------------------INSERT--------------------

    #insert cognito users
    # print("\n\n--------------------INSERTING COGNITO USERS--------------------")
    # To disable randomly generated rows, add False argument to all except staffs & pwas
    staffs = get_staffs()
    vols = get_volunteers(staffs)
    pwas = get_pwas()
    projects = get_projects(vols,staffs,pwas)
    recurring = get_recurring(projects)
    events = get_events(projects)
    try:
        success = True
        role = "core_team"
        for i in range (1,len(staffs) - 1):
            data = {
                "input": {
                    "email": f"person{i}@aphasia.sg",
                    "password": f"Passwordperson{i}!",
                    "role": role,
                    "user_id": f"{i}"
                }
            }
            r = requests.post(insert_cognito_users, data = json.dumps(data))

            if r.status_code != 200:
                print(r.text)
                success = False

            if i == 3:
                role = "core_volunteer"
            elif i == 6:
                role = "intern"
            elif i == 9:
                role = "core_team"

        data = {
            "input": {
                "email": "arixgg@gmail.com",
                "password": "Password1!",
                "role": "core_team",
                "user_id": str(len(staffs) - 1)
            }
        }
        r = requests.post(insert_cognito_users, data = json.dumps(data))

        data = {
            "input": {
                "email": "admin@gmail.com",
                "password": "Password1!",
                "role": "admin",
                "user_id": str(len(staffs))
            }
        }
        r = requests.post(insert_cognito_users, data = json.dumps(data))

        if r.status_code != 200:
            print(r.text)
            success = False

    except Exception as e:
        print(e)
        success = False

    success = True

    #insert languages
    insert_query = """
        mutation {
            insert_languages(objects: [{language: "English", description: "English"},{language: "Chinese_Mandarin", description: "Chinese Mandarin"},{language: "Malay", description: "Malay"},{language: "Tamil", description: "Tamil"},{language: "Cantonese", description: "Cantonese"},{language: "Hokkien", description: "Hokkien"},{language: "Teochew", description: "Teochew"},{language: "Hainanese", description: "Hainanese"},{language: "Hakka", description: "Hakka"},{language: "Foochow", description: "Foochow"},{language: "Bahasa_Indonesian", description: "Bahasa Indonesian"},{language: "Burmese", description: "Burmese"},{language: "Javanese", description: "Javanese"},{language: "Tagalog", description: "Tagalog"},{language: "Thai", description: "Thai"},{language: "Vietnamese", description: "Vietnamese"},{language: "Hindi", description: "Hindi"},{language: "Punjabi", description: "Punjabi"},{language: "Bengali", description: "Bengali"},{language: "Nepali", description: "Nepali"},{language: "Sinhala", description: "Sinhala"},{language: "Urdu", description: "Urdu"},{language: "Japanese", description: "Japanese"},{language: "Korean", description: "Korean"},{language: "Arabic", description: "Arabic"},{language: "Dutch", description: "Dutch"},{language: "French", description: "French"},{language: "German", description: "German"},{language: "Portugese", description: "Portugese"},{language: "Russian", description: "Russian"},{language: "Spanish", description: "Spanish"}], on_conflict: {constraint: languages_pkey, update_columns: description}) {
                affected_rows
            }

            """

    #insert status
    insert_query += """
            insert_status(objects: [{status: "Pending Approval"},{status: "Approved"},{status: "KIV"},{status: "Rejected"}]) {
                affected_rows
            }
            """

    #insert roles
    insert_query += """
            insert_roles(objects: [{role: "intern", description: "Intern"}, {role: "core_team", description: "Core Team"}, {role: "core_volunteer", description: "Core Volunteer"}, {role: "admin", description: "Admin"}], on_conflict: {constraint: roles_pkey, update_columns: description}) {
                affected_rows
            }
            """

    #insert channels
    insert_query += """
        insert_channels(objects: [{channel: "Facebook"}, {channel: "Instagram"}, {channel: "Twitter"},{channel: "Linkedin"},{channel: "Public Outreach"},{channel: "Workshops/Talks" },{channel: "Patients/Caregivers" },{channel: "School" },{channel: "Other Volunteers" },{channel: "Radio" },{channel: "Our Website" },{channel: "Speech Therapist" },{channel: "Other Healthcare Professionals" },{channel: "Newspaper" },{channel: "Hospital Advertisement" },{channel: "Word Of Mouth" },{channel: "Day Care Centre" },{channel: "Doctor" }]) {
            affected_rows
        }
        """

    #insert pwa_contact_status
    insert_query += """
        insert_pwa_contact_status(objects: [{status: "Not Contacted"},{status: "Contacted but no response"},{status: "Contacted"}]){
            affected_rows
        }
        """

    #insert project_task_status
    insert_query += """
        insert_project_task_status(objects: [{status: "Completed"},{status: "In-progress"},{status: "To-do"}]){
            affected_rows
        }
        """

    #insert voltypes
    insert_query += """
        insert_voltypes(objects: [{type: "Befriender", description: "Befriender"}, {type: "Project_Volunteer", description: "Project Volunteer"}], on_conflict: {constraint: voltypes_pkey, update_columns: description}) {
            affected_rows
        }
    }
        """

    print("\n\n--------------------INSERTING FIXED DATA--------------------")
    execute_query(insert_query)

    #insert staffs
    insert_query = """
    mutation ($staffs: [staffs_insert_input!]!, $vols: [volunteers_insert_input!]!, $pwas: [pwas_insert_input!]!, $projects: [projects_insert_input!]!, $recurring: [recurring_insert_input!]!, $events: [events_insert_input!]!) {
        insert_staffs(objects: $staffs) {
            affected_rows
        }
        """
    data = {"staffs": staffs}

    # insert volunteers
    insert_query += """
        insert_volunteers(objects: $vols) {
            affected_rows
        }
            """
    data['vols'] = vols

    # insert PWAs
    insert_query += """
        insert_pwas(objects: $pwas) {
            affected_rows
        }
            """
    data['pwas'] = pwas

    #insert projects
    insert_query += """
        insert_projects(objects: $projects) {
            affected_rows
        }
        """
    data['projects'] = projects

    #insert recurr
    insert_query += """
        insert_recurring(objects: $recurring) {
            affected_rows
        }
        """

    data['recurring'] = recurring

    #insert events
    insert_query += """
        insert_events(objects: $events) {
            affected_rows
        }
        """
    data['events'] = events

    insert_query += "}"

    print("\n\n--------------------INSERTING DYNAMIC DATA--------------------")

    execute_query_with_variables(insert_query, data)

def lambda_handler(event, context):
    delete()
    alter_sequence()
    insert()
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": "Bootstrap successful, see Cloudwatch logs for more details"
    }