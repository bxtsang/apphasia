import json
import os
import requests

# hasura credentials
HASURA_URI = "https://aphasia-hasura-dev.herokuapp.com/v1/graphql"
HASURA_URI_SQL = "https://aphasia-hasura-dev.herokuapp.com/v1/graphql"
HASURA_ADMIN_SECRET = "pwayismyhome12061997"
HASURA_HEADERS = { "Content-Type": "application/json", "x-hasura-admin-secret": HASURA_ADMIN_SECRET }

# api endpoints
delete_cognito_users = "https://bnpzp70foh.execute-api.ap-southeast-1.amazonaws.com/dev"
insert_cognito_users = "https://jvuzedyfme.execute-api.ap-southeast-1.amazonaws.com/test"

def execute_query(query, sql=False):
    success = True
    try:
        r = requests.post(HASURA_URI_SQL if sql else HASURA_URI, json = {'query' : query}, headers = HASURA_HEADERS)

        if r.status_code != 200:
            print(r.text)
            success = False

    except Exception as e:
        print(e)
        success = False

    print("success!") if success else print("error")

def bootstrap():
    #--------------------DELETE--------------------


    #delete cognito users
    print("\n\n--------------------DELETING COGNITO USERS--------------------")
    try:
        success = True
        for i in range (1,4):
            data = {
                "input" : {
                    "email": f"person{i}@aphasia.sg",
                    "user_id": f"{i}"
                }
            }
            r = requests.post(delete_cognito_users, data = json.dumps(data))

            if r.status_code != 200:
                print(r.text)
                success = False

    except Exception as e:
        print(e)
        success = False

    print("success!") if success else print("error")
    success = True

    #delete hasura data
    print("\n\n--------------------DELETING HASURA DATA--------------------")

    #delete staff_languages
    print("\n\n--------------------DELETING staff_languages DATA--------------------")
    query = """
    mutation {
        delete_staff_languages(where: {}) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #delete vol_languages
    print("\n\n--------------------DELETING vol_languages DATA--------------------")
    query = """
    mutation {
        delete_vol_languages(where: {}) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #delete vol_channels
    print("\n\n--------------------DELETING vol_channels DATA--------------------")
    query = """
    mutation {
        delete_vol_channels(where: {}) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #delete vol_supervisors
    print("\n\n--------------------DELETING vol_supervisors DATA--------------------")
    query = """
    mutation MyMutation {
        delete_vol_supervisors(where: {}) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #delete staff_supervisors
    print("\n\n--------------------DELETING staff_supervisors DATA--------------------")
    query = """
    mutation {
        delete_staff_supervisors(where: {}) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #delete project_staffs
    print("\n\n--------------------DELETING project_staffs DATA--------------------")
    query = """
    mutation {
        delete_project_staffs(where: {}) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #delete projects
    print("\n\n--------------------DELETING projects DATA--------------------")
    query = """
    mutation {
        delete_projects(where: {}) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #delete project_vol
    print("\n\n--------------------DELETING project_vol DATA--------------------")
    query = """
    mutation {
        delete_project_vol(where: {}) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #delete staffs
    print("\n\n--------------------DELETING staffs DATA--------------------")
    query = """
    mutation {
        delete_staffs(where: {}) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #delete channels
    print("\n\n--------------------DELETING channels DATA--------------------")
    query = """
    mutation {
        delete_channels(where: {}) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #delete voltypes
    print("\n\n--------------------DELETING voltypes DATA--------------------")
    query = """
    mutation MyMutation2 {
        delete_voltypes(where: {}) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #delete languages
    print("\n\n--------------------DELETING languages DATA--------------------")
    query = """
    mutation {
        delete_languages(where: {}) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #delete roles
    print("\n\n--------------------DELETING roles DATA--------------------")
    query = """
    mutation {
        delete_roles(where: {}) {
            affected_rows
        }
    }
            """
    execute_query(query)


    #--------------------ALTER--------------------


    #alter staffs_id_seq
    print("\n\n--------------------ALTERING staffs_id_seq SEQUENCE--------------------")
    query = """
    {
        "type": "run_sql",
        "args": {
            "sql": "ALTER SEQUENCE staffs_id_seq RESTART 4;"
        }
    }
            """
    execute_sql_query(query, True)

    #alter projects_id_seq
    print("\n\n--------------------ALTERING projects_id_seq SEQUENCE--------------------")
    query = """
    {
        "type": "run_sql",
        "args": {
            "sql": "ALTER SEQUENCE projects_id_seq RESTART 4;"
        }
    }
            """
    execute_query(query, True)

    #alter volunteers_id_seq
    print("\n\n--------------------ALTERING volunteers_id_seq SEQUENCE--------------------")
    query = """
    {
        "type": "run_sql",
        "args": {
            "sql": "ALTER SEQUENCE volunteers_id_seq RESTART 4;"
        }
    }
            """
    execute_query(query)

    #--------------------INSERT--------------------

    #insert cognito users
    print("\n\n--------------------INSERTING COGNITO USERS--------------------")
    try:
        success = True
        for i in range (1,4):
            data = {
                "input": {
                    "email": f"person{i}@aphasia.sg",
                    "password": f"passwordperson{i}",
                    "role": "core_team",
                    "user_id": f"{i}"
                }
            }
            r = requests.post(insert, data = json.dumps(data))

            if r.status_code != 200:
                print(r.text)
                success = False

    except Exception as e:
        print(e)
        success = False

    print("success!") if success else print("error")
    success = True

    #insert languages
    print("\n\n--------------------INSERTING languages DATA--------------------")
    query = """
        mutation {
            insert_languages(
                objects: [{language: "Abkhaz"},{language: "Afar"},{language: "Afrikaans"},{language: "Akan"},{language: "Albanian"},{language: "Amharic"},{language: "Arabic"},{language: "Aragonese"},{language: "Armenian"},{language: "Assamese"},{language: "Avaric"},{language: "Avestan"},{language: "Aymara"},{language: "Azerbaijani"},{language: "Bambara"},{language: "Bashkir"},{language: "Basque"},{language: "Belarusian"},{language: "Bengali"},{language: "Bihari"},{language: "Bislama"},{language: "Bosnian"},{language: "Breton"},{language: "Bulgarian"},{language: "Burmese"},{language: "Catalan"},{language: "Chamorro"},{language: "Chechen"},{language: "Chichewa"},{language: "Chinese"},{language: "Chuvash"},{language: "Cornish"},{language: "Corsican"},{language: "Cree"},{language: "Croatian"},{language: "Czech"},{language: "Danish"},{language: "Divehi"},{language: "Dutch"},{language: "English"},{language: "Esperanto"},{language: "Estonian"},{language: "Ewe"},{language: "Faroese"},{language: "Fijian"},{language: "Finnish"},{language: "French"},{language: "Fula"},{language: "Galician"},{language: "Georgian"},{language: "German"},{language: "Greek"},{language: "Guarani"},{language: "Gujarati"},{language: "Haitian"},{language: "Hausa"},{language: "Hebrew"},{language: "Herero"},{language: "Hindi"},{language: "Hiri_Motu"},{language: "Hungarian"},{language: "Interlingua"},{language: "Indonesian"},{language: "Interlingue"},{language: "Irish"},{language: "Igbo"},{language: "Inupiaq"},{language: "Ido"},{language: "Icelandic"},{language: "Italian"},{language: "Inuktitut"},{language: "Japanese"},{language: "Javanese"},{language: "Kalaallisut"},{language: "Kannada"},{language: "Kanuri"},{language: "Kashmiri"},{language: "Kazakh"},{language: "Khmer"},{language: "Kikuyu"},{language: "Kinyarwanda"},{language: "Kirghiz"},{language: "Komi"},{language: "Kongo"},{language: "Korean"},{language: "Kurdish"},{language: "Kwanyama"},{language: "Latin"},{language: "Luxembourgish"},{language: "Luganda"},{language: "Limburgish"},{language: "Lingala"},{language: "Lao"},{language: "Lithuanian"},{language: "Luba_Katanga"},{language: "Latvian"},{language: "Manx"},{language: "Macedonian"},{language: "Malagasy"},{language: "Malay"},{language: "Malayalam"},{language: "Maltese"},{language: "Maori"},{language: "Marathi"},{language: "Marshallese"},{language: "Mongolian"},{language: "Nauru"},{language: "Navajo"},{language: "Norwegian_Bokmal"},{language: "North_Ndebele"},{language: "Nepali"},{language: "Ndonga"},{language: "Norwegian_Nynorsk"},{language: "Norwegian"},{language: "Nuosu"},{language: "South_Ndebele"},{language: "Occitan"},{language: "Ojibwe"},{language: "Old_Church_Slavonic"},{language: "Oromo"},{language: "Oriya"},{language: "Ossetian"},{language: "Punjabi"},{language: "Pali"},{language: "Persian"},{language: "Polish"},{language: "Pashto"},{language: "Portuguese"},{language: "Quechua"},{language: "Romansh"},{language: "Kirundi"},{language: "Romanian"},{language: "Russian"},{language: "Sanskrit"},{language: "Sardinian"},{language: "Sindhi"},{language: "Northern_Sami"},{language: "Samoan"},{language: "Sango"},{language: "Serbian"},{language: "Gaelic"},{language: "Shona"},{language: "Sinhala"},{language: "Slovak"},{language: "Slovene"},{language: "Somali"},{language: "Southern_Sotho"},{language: "Spanish"},{language: "Sundanese"},{language: "Swahili"},{language: "Swati"},{language: "Swedish"},{language: "Tamil"},{language: "Telugu"},{language: "Tajik"},{language: "Thai"},{language: "Tigrinya"},{language: "Tibetan"},{language: "Turkmen"},{language: "Tagalog"},{language: "Tswana"},{language: "Tonga"},{language: "Turkish"},{language: "Tsonga"},{language: "Tatar"},{language: "Twi"},{language: "Tahitian"},{language: "Uyghur"},{language: "Ukrainian"},{language: "Urdu"},{language: "Uzbek"},{language: "Venda"},{language: "Vietnamese"},{language: "Volapuk"},{language: "Walloon"},{language: "Welsh"},{language: "Wolof"},{language: "Western_Frisian"},{language: "Xhosa"},{language: "Yiddish"},{language: "Yoruba"},{language: "Zhuang"},{language: "Cantonese"},{language: "Hokkien"},{language: "Teochew"}]
            ) {
                affected_rows
            }
        }

            """
    execute_query(query)

    #insert roles
    print("\n\n--------------------INSERTING roles DATA--------------------")
    query = """
        mutation {
            insert_roles(objects: [{ role: "intern" }, { role: "core_team" }, { role: "core_volunteer" }]) {
                affected_rows
            }
        }
            """
    execute_query(query)

    #insert channels
    print("\n\n--------------------INSERTING channels DATA--------------------")
    query = """
    mutation {
        insert_channels(objects: [{channel: "facebook"}, {channel: "instagram"}, {channel: "twitter"}]) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #insert voltypes
    print("\n\n--------------------INSERTING voltypes DATA--------------------")
    query = """
    mutation {
        insert_voltypes(objects: [{type: "Befriender"}, {type: "Project_Volunteer"}]) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #insert staffs
    print("\n\n--------------------INSERTING staffs DATA--------------------")
    query = """
    mutation {
        insert_staffs(objects: [{address: "69 Geylang Rd", id: 2, bio: "Person 2", contact_num: 87654321, email: "person2@aphasia.sg", name: "Tom Dick", dob: "1909-12-01", gender: "F", profession: "Student", nric: "S0000000B", role: core_volunteer, date_joined: "2020-01-14"}, {address: "123 Fake Street", id: 1, bio: "Person 1", contact_num: 12345678, email: "person1@aphasia.sg", name: "Bob Billy", dob: "1999-01-12", gender: "M", profession: "Student", nric: "S9999999B", role: core_team, date_joined: "2021-01-15"},{address: "456 Hip Road", id: 3, bio: "Person 3", contact_num: 13579246, email: "person3@aphasia.sg", name: "James Jones", dob: "1965-09-15", gender: "M", profession: "Financial Advisor", nric: "SXXXXXXXD", role: intern, date_joined: "2020-01-19"}]) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #insert volunteers
    print("\n\n--------------------INSERTING volunteers DATA--------------------")
    query = """
    mutation {
        insert_volunteers(objects: [{bio: "Sacrificial volunteer 1", contact_num: 11111111, date_joined: "2021-01-21", dob: "1921-01-20", email: "vol1@aphasia.sg", gender: "F", id: 1, is_active: true, name: "Donald Trump", nickname: "Volunteer 1", profession: "President", status: 1, is_speech_therapist: true, ws_place: "The White House"},{bio: "Bad boi volunteer 2", contact_num: 22222222, date_joined: "2020-01-21", dob: "1964-04-16", email: "vol2@aphasia.sg", gender: "M", id: 2, is_active: true, name: "Thomas Edison", nickname: "Volunteer 2", profession: "Scientist", status: 0},{bio: "Bored Volunteer 3", contact_num: 333333333, date_joined: "2021-01-01", dob: "1997-09-15", email: "vol3@aphasia.sg", gender: "F", id: 3, is_active: false, name: "Harry Potter", nickname: "Volunteer 3", profession: "Wizard", status: 0, ws_place: "Hogwarts"}]) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #insert projects
    print("\n\n--------------------INSERTING projects DATA--------------------")
    query = """
    mutation {
        insert_projects(objects: [{owner_id: 1, id: 1, title: "My favourite project"}, {owner_id: 2, id: 2, title: "Hello World"},{owner_id: 1, id: 3, title: "Chit Chat Initiative"}]) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #insert staff_languages
    print("\n\n--------------------INSERTING staff_languages DATA--------------------")
    query = """
    mutation {
        insert_staff_languages(objects: [{language: Chinese, staff_id: 1}, {language: Chinese, staff_id: 2}, {language: English, staff_id: 2}]) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #insert vol_languages
    print("\n\n--------------------INSERTING vol_languages DATA--------------------")
    query = """
    mutation {
        insert_vol_languages(objects: [{language: Chinese, vol_id: 1}, {language: Chinese, vol_id: 3}, {language: English, vol_id: 2}]) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #insert vol_supervisors
    print("\n\n--------------------INSERTING vol_supervisors DATA--------------------")
    query = """
    mutation {
        insert_vol_supervisors(objects: [{staff_id: 1, vol_id: 1},{staff_id: 1, vol_id: 2},{staff_id: 1, vol_id: 3}]) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #insert vol_channels
    print("\n\n--------------------INSERTING vol_channels DATA--------------------")
    query = """
    mutation {
        insert_vol_channels(objects: [{channels: instagram, vol_id: 1}, {channels: facebook, vol_id: 1}, {channels: instagram, vol_id: 2}]) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #insert vol_voltypes
    print("\n\n--------------------INSERTING vol_voltypes DATA--------------------")
    query = """
    mutation {
        insert_vol_voltypes(objects: [{vol_id: 1, voltype: Befriender}, {vol_id: 2, voltype: Befriender}, {vol_id: 1, voltype: Project_Volunteer}]) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #insert staff_supervisors
    print("\n\n--------------------INSERTING staff_supervisors DATA--------------------")
    query = """
    mutation {
        insert_staff_supervisors(objects: {staff_id: 1, supervisor_id: 2}) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #insert project_staffs
    print("\n\n--------------------INSERTING project_staffs DATA--------------------")
    query = """
    mutation {
        insert_project_staffs(objects: [{project_id: 1, staff_id: 2}, {project_id: 1, staff_id: 3}, {project_id: 2, staff_id: 3}]) {
            affected_rows
        }
    }
            """
    execute_query(query)

    #insert project_vol
    print("\n\n--------------------INSERTING project_vol DATA--------------------")
    query = """
    mutation {
        insert_project_vol(objects: [{project_id: 1, vol_id: 1}, {project_id: 1, vol_id: 2}, {project_id: 1, vol_id: 3}, {project_id: 3, vol_id: 2}, {project_id: 3, vol_id: 3}]) {
            affected_rows
        }
    }
            """
    execute_query(query)

bootstrap()
