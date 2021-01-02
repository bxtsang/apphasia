from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import os
import requests
from Google import Create_Service

app = Flask(__name__)

CLIENT_SECRET_FILE = "credentials.json"
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# request.args: the key/value pairs in the URL query string
# request.form: the key/value pairs in the body, from a HTML post form, or JavaScript request that isn't JSON encoded
# request.files: the files in the body, which Flask keeps separate from form. HTML forms must use enctype=multipart/form-data or files will not be uploaded.
# request.values: combined args and form, preferring args if keys overlap
# request.json: parsed JSON data. The request must have the application/json content type, or use request.get_json(force=True) to ignore the content type.
# All of these are MultiDict instances (except for json). You can access values using:

# request.form['name']: use indexing if you know the key exists
# request.form.get('name'): use get if the key might not exist
# request.form.getlist('name'): use getlist if the key is sent multiple times and you want a list of values. get only returns the first value.

@app.route('/folder', methods = ['POST'])
def create_folders():
    folders = request.json['folders']
    print(folders)
    result = {}
    id_list = []

    for folder in folders:
        file_metadata = {
            'name' : folder,
            'mimeType' : "application/vnd.google-apps.folder"
        }

        id_list.append(SERVICE.files().create(body=file_metadata).execute()['id'])

    result['id_list'] = id_list
    return result

@app.route('/folder', methods = ['GET'])
def search_all_folders():
    result = {}
    folders = []

    page_token = None

    while True:
        response = SERVICE.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)',
                                            pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            folders.append(file)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    result['folders'] = folders
    return result

def create_folder_in_folder(parent, child):
    page_token = None
    while True:
        response = SERVICE.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)',
                                            pageToken=page_token).execute()

        for file in response.get('files', []):
            # Process change
            if (file.get('name') == parent):
                print ('[TARGET FILE FOUND]: %s (%s)' % (file.get('name'), file.get('id')))
                file_metadata = {
                'name': child,
                'mimeType' : 'application/vnd.google-apps.folder',
                'parents' : [file.get('id')]
                }

                SERVICE.files().create(body=file_metadata).execute()


            else:
                print ('file found: %s (%s)' % (file.get('name'), file.get('id')))



        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
        
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5400, debug=True)
