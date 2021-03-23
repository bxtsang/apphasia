import json
import os
import requests
import json
import boto3
from datetime import *

# hasura credentials
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

        return  response

    except Exception as e:
        print(e)
        success = False
        return "error occurred"

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

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def calculate_mean(my_list):
    total = 0
    count = 0
    for peep in my_list:
        total += peep[2]
        count += 1

    return round(total/count)

def lambda_handler(event, context):
    try:
        event_body = json.loads(event['body']) if "body" in event and event['body'] else {"resources": "pwas"}
        resources = event_body['resources'] if 'resources' in event_body else "pwas" 
        today = datetime.now()
        year_ago = today - timedelta(days=365)
        six_months_ago = today - timedelta(days=365/2)
        three_months_ago = today - timedelta(days=365/4)
        month_ago = today - timedelta(days=30)
        times = [month_ago,three_months_ago,six_months_ago,year_ago]
        query = """
        query {
            volunteers: people_external(where: {volunteer_details: {}}) {
                name
                id
                dob
                volunteer_details {
                profession
                vol_languages {
                    languages {
                    description
                    }
                }
                }
            }
            pwas: people_external(where: {pwa_details: {}}) {
                name
                id
                dob
                pwa_details {
                wheelchair
                languages {
                    languages {
                    description
                    }
                }
                }
            }
            projects {
                title
                pwas {
                pwa_id
                }
                volunteers {
                vol_id
                }
            }
            events {
                date
                project {
                    id
                    title
                }
                pwas {
                    project_id
                    pwa_id
                }
                volunteers {
                    vol_id
                    project_id
                }
                recurring {
                    pwas {
                        project_id
                        pwa_id
                    }
                    volunteers {
                        vol_id
                        project_id
                    }
                }
            }
        }
        """
        result = execute_query(query)
        result_volunteers = result['data']['volunteers']
        result_pwas = result['data']['pwas']
        result_events = result['data']['events']
        projects = result['data']['projects']

        # Generate overall volunteer details
        professions = {
            'Speech and Langauge Therapist (SLT)': 'Speech and Langauge Therapist (SLT)',
            'Music Therapist': 'Music Therapist',
            'Occupational Therapist': 'Occupational Therapist',
            'Social Worker': 'Social Worker',
            'Healthcare professional (but none of the above)': "Healthcare professional",
            'SLT Student': "SLT Student",
            'Student (but not in the field of speech therapy)': 'Student (but not in the field of speech therapy)'
        }
        volunteers_list = []
        volunteers_dict = {}
        vol_languages = {}
        vol_professions = {}
        volunteers_events = {
            "# of total events attended this year": {},
            "# of total events attended this month": {}
        }
        volunteers_attrition = {
            "Volunteers who have not joined an event in the past month": [],
            "Volunteers who have not joined an event in the past 3 months": [],
            "Volunteers who have not joined an event in the past 6 months": [],
            "Volunteers who have not joined an event in the past year": []
        }
        vol_attrition_keys = [ch for ch in volunteers_attrition]
        for vol in result_volunteers:
            # Generate id,name and age details
            vol_id = vol['id']
            name = vol['name']
            age = calculate_age(date(*[int(ch) for ch in vol['dob'].split("-")]))
            volunteers_list.append([vol_id, name, age])
            volunteers_dict[vol_id] = [vol_id, name, age]
            profession = vol['volunteer_details']['profession']
            
            # Add volunteer to attrition for future computing use
            for attr in volunteers_attrition:
                volunteers_attrition[attr].append(name)

            # Generate profession
            if profession not in professions:
                profession = "Laypeople"
            if profession not in vol_professions:
                vol_professions[profession] = [name]
            else:
                vol_professions[profession].append(name)

            # Generate languages details
            for lang in vol['volunteer_details']['vol_languages']:
                vol_lang = lang['languages']['description']
                if vol_lang in vol_languages:
                    vol_languages[vol_lang].append(name)
                else:
                    vol_languages[vol_lang] = [name]

        volunteers_list.sort(key=lambda x:x[2])
        mean_vol_age = calculate_mean(volunteers_list)

        # Generate overall pwa details
        pwas_list = []
        pwas_dict = {}
        pwa_languages = {}
        pwa_wheelchair = []
        pwas_attrition = {
            "PWAs who have not joined an event in the past month": [],
            "PWAs who have not joined an event in the past 3 months": [],
            "PWAs who have not joined an event in the past 6 months": [],
            "PWAs who have not joined an event in the past year": []
        }
        pwas_attrition_keys = [ch for ch in pwas_attrition]

        pwas_events = {
            "# of total events attended this year": {},
            "# of total events attended this month": {}
        }

        for pwa in result_pwas:
            # Generate id, name and age
            pwa_id = pwa['id']
            name = pwa['name']
            age = calculate_age(date(*[int(ch) for ch in pwa['dob'].split("-")]))
            pwas_list.append([pwa_id, name, age])
            pwas_dict[pwa_id] = [pwa_id, name, age]

            # Add pwas to attrition for future computing use
            for attr in pwas_attrition:
                pwas_attrition[attr].append(name)

            # Generate wheelchair details
            if pwa['pwa_details']['wheelchair']:
                pwa_wheelchair.append(name)

            # Generate language details
            for lang in pwa['pwa_details']['languages']:
                pwa_lang = lang['languages']['description']
                if pwa_lang in pwa_languages:
                    pwa_languages[pwa_lang].append(name)
                else:
                    pwa_languages[pwa_lang] = [name]

        project_events = {}
        if pwas_list:
            pwas_list.sort(key=lambda x:x[2])
            mean_pwa_age = calculate_mean(pwas_list)
    
            
            pwa_capture_age = {
                "Mean age of PWAs overall": mean_pwa_age,
                "Name of youngest PWAs overall": pwas_list[0][1],
                "Name of oldest PWAs overall": pwas_list[-1][1],
                "Age range of PWAs overall": f"{pwas_list[0][2]} - {pwas_list[-1][2]}"
            }
        else:
            pwa_capture_age = {}

        if volunteers_list:
            vol_capture_age = {
                "Mean age of volunteers overall": mean_vol_age,
                "Name of youngest volunteer overall": volunteers_list[0][1],
                "Name of oldest volunteer overall": volunteers_list[-1][1],
                "Age range of volunteers overall": f"{volunteers_list[0][2]} - {volunteers_list[-1][2]}"
            }
        else:
            vol_capture_age = {}

        for proj in projects:
            title = proj['title']
            title_year_key = f"# of {title} sessions attended this year"
            title_month_key = f"# of {title} sessions attended this month"

            # Create title for attendance tracking
            if title_year_key not in volunteers_events:
                volunteers_events[title_year_key] = {}
                volunteers_events[title_month_key] = {}
                pwas_events[title_year_key] = {}
                pwas_events[title_month_key] = {}

            # Generate project volunteer details
            volunteers = []
            for vol in proj['volunteers']:
                vol_id = vol['vol_id']
                volunteers.append(volunteers_dict[vol_id])
            
            if volunteers:
                volunteers.sort(key=lambda x:x[2])
                vol_capture_age[f"Mean age of volunteers for {proj['title']}"] = calculate_mean(volunteers)
                vol_capture_age[f"Name of youngest volunteer for {proj['title']}"] = volunteers[0][1]
                vol_capture_age[f"Name of oldest volunteer for {proj['title']}"] = volunteers[-1][1]
                vol_capture_age[f"Age range of volunteers for {proj['title']}"] = f"{volunteers[0][2]} - {volunteers[-1][2]}"

            # Generate project PWAs details
            pwas = []
            for pwa in proj['pwas']:
                pwa_id = pwa['pwa_id']
                pwas.append(pwas_dict[pwa_id])
            
            if pwas:
                pwas.sort(key=lambda x:x[2])
                pwa_capture_age[f"Mean age of PWAs for {proj['title']}"] = calculate_mean(pwas)
                pwa_capture_age[f"Name of youngest PWAs for {proj['title']}"] = pwas[0][1]
                pwa_capture_age[f"Name of oldest PWAs for {proj['title']}"] = pwas[-1][1]
                pwa_capture_age[f"Age range of PWAs for {proj['title']}"] = f"{pwas[0][2]} - {pwas[-1][2]}"

        # Generate event details
        for event in result_events:
            event_date = date(*[int(ch) for ch in event['date'].split("-")])
            title = event['project']['title']
            vols = []
            pwas = []

            # Get volunteers attending that event
            if event['volunteers']:
                for vol in event['volunteers']:
                    vols.append(vol["vol_id"])
            elif event['recurring']:
                for vol in event['recurring']['volunteers']:
                    vols.append(vol[ 'vol_id'])

            # Get PWAs attending that event
            if event['pwas']:
                for pwa in event['pwas']:
                    pwas.append(pwa["pwa_id"])
            elif event['recurring']:
                for pwa in event['recurring']['pwas']:
                    pwas.append(pwa[ 'pwa_id'])

            for vol in vols:
                vol_name = volunteers_dict[vol][1]

                # No. of events attended for volunteers this year
                if event_date.year == today.year and event_date <= today.date():
                    title_year_key = f"# of {title} sessions attended this year"
                    title_month_key = f"# of {title} sessions attended this month"
                    all_year = "# of total events attended this year"
                    all_month = "# of total events attended this month"

                    if vol_name not in volunteers_events[title_year_key]:
                        volunteers_events[title_year_key][vol_name] = 0

                    volunteers_events[title_year_key][vol_name] += 1

                    if vol_name not in volunteers_events[all_year]:
                        volunteers_events[all_year][vol_name] = 0

                    volunteers_events[all_year][vol_name] += 1
                    # No. of events attended for volunteers this month
                    if event_date.month == today.month:
                        if vol_name not in volunteers_events[title_month_key]:
                            volunteers_events[title_month_key][vol_name] = 0

                        volunteers_events[title_month_key][vol_name] += 1

                        if vol_name not in volunteers_events[all_month]:
                            volunteers_events[all_month][vol_name] = 0

                        volunteers_events[all_month][vol_name] += 1

                for i in range(len(times)):
                    if event_date >= times[i].date() and vol_name in volunteers_attrition[vol_attrition_keys[i]]:
                        volunteers_attrition[vol_attrition_keys[i]].remove(vol_name)


            for pwa in pwas:
                pwa_name = pwas_dict[pwa][1]

                # No. of events attended for pwas this year
                if event_date.year == today.year and event_date <= today.date():
                    title_year_key = f"# of {title} sessions attended this year"
                    title_month_key = f"# of {title} sessions attended this month"
                    all_year = "# of total events attended this year"
                    all_month = "# of total events attended this month"
                    if pwa_name not in pwas_events[title_year_key]:
                        pwas_events[title_year_key][pwa_name] = 0

                    pwas_events[title_year_key][pwa_name] += 1

                    if pwa_name not in pwas_events[all_year]:
                        pwas_events[all_year][pwa_name] = 0

                    pwas_events[all_year][pwa_name] += 1

                    # No. of events attended for pwas this month
                    if event_date.month == today.month:
                        if pwa_name not in pwas_events[title_month_key]:
                            pwas_events[title_month_key][pwa_name] = 0

                        pwas_events[title_month_key][pwa_name] += 1

                        if pwa_name not in pwas_events[all_month]:
                            pwas_events[all_month][pwa_name] = 0

                        pwas_events[all_month][pwa_name] += 1
                    
                for i in range(len(times)):
                    if event_date >= times[i].date() and pwa_name in pwas_attrition[pwas_attrition_keys[i]]:
                        pwas_attrition[pwas_attrition_keys[i]].remove(pwa_name)

                    
            # Count events of each project
            if title not in project_events: 
                project_events[title] = 1
            else:
                project_events[title] += 1

        result = {
            "volunteers": {
                "Attendance Tracking": volunteers_events,
                "Capture Age": vol_capture_age,
                "Capture attrition rate": volunteers_attrition,
                "Language proficiency": vol_languages,
                "Volunteer profile": vol_professions
            },
            "pwas": {
                "Attendance Tracking": pwas_events,
                "Capture Age": pwa_capture_age,
                "Capture attrition rate": pwas_attrition,
                "Language proficiency": pwa_languages,
                "PWA profile": {
                    "PWAs who require a wheelchair": pwa_wheelchair
                }
            },
            "projects": project_events
        }
        
        add_zero = ["volunteers","pwas"]
        for entity in add_zero:
            for ch in result[entity]['Attendance Tracking']:
                header = result[entity]['Attendance Tracking'][ch]
                loop = volunteers_list
                if entity == "pwas":
                    loop = pwas_list
                for ent in loop:
                    if ent[1] not in header:
                        header[ent[1]] = 0
        return {
            'statusCode': 200,
            'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps(result[resources] if resources in result else result['pwas'])
        }
    except Exception as e:
        raise e
        return {
            'statusCode': 500,
            'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
            },
            'body': "Internal server error"
        }
