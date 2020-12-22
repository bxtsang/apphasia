from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import os
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbURL')
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@localhost:3306/volunteer"
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

class Volunteer(db.Model):
    __tablename__ = "volunteer"

    userID = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.Integer())
    password = db.Column(db.String(128), nullable=False)

    def get_json(self):
        return {'userID': self.userID, 'name': self.name, 'email': self.email, 'phone': self.phone, 'password': self.password}


@app.route("/volunteer/<userID>", methods=["GET"])
def getVolunteer(userID):
    result = {}

    volunteer = Volunteer.query.filter_by(userID = userID).first()

    print(f"\nRetrieving data for volunteer with userID: {userID}...\n")

    if not volunteer:
        result["result"] = "failed"
        result["reason"] = "No such user exists"
        return jsonify(result), 500

    result["result"] = "success"
    result["user"] = volunteer.get_json()

    return jsonify(result)

@app.route("/volunteer", methods=["GET"])
def getAllVolunteer():
    volunteers = Volunteer.query.all()
    volunteerList = []
    result = {}

    print(f"\nReturning all volunteer data...\n")

    for volunteer in volunteers:
        volunteerList.append(volunteer.get_json())

    result['result'] = "success"
    result['users'] = volunteerList

    return jsonify(result), 200

@app.route("/volunteer", methods=["POST"])
def addVolunteer():
    result = {}
    data = request.get_json()
    name = data['name']
    email = data['email']
    phone = data['phone']
    password = data['password']

    if not data or not name or not email or not phone or not password:
        result["result"] = "failed"
        result["reason"] = "One or more fields are empty."
        return jsonify(result), 500

    volunteer = Volunteer(name = name, email = email, phone = phone, password = password)

    print(f"\nAdding new volunteer member {name}...\n")

    db.session.add(volunteer)
    db.session.commit()

    result["result"] = "success"
    result["user"] = volunteer.get_json()
    return jsonify(result), 200

@app.route("/volunteer", methods=["DELETE"])
def removeVolunteer():
    result = {}
    data = request.get_json()
    email = data['email']

    if not email:
        result["result"] = "failed"
        result["reason"] = "Email field is empty."
        return jsonify(result), 500

    volunteer = Volunteer.query.filter_by(email = email).first()

    print(f"\nDeleteing volunteer member with email: {email}...\n")

    if not volunteer:
        result["result"] = "failed"
        result["reason"] = "User does not exist."
        return jsonify(result), 404

    Volunteer.query.filter_by(email = email).delete()

    result["result"] = "success"
    return jsonify(result),200

@app.route("/volunteer", methods=["PUT"])
def updateVolunteer():
    result = {}
    data = request.get_json()
    name = data['name']
    email = data['email']
    phone = data['phone']
    password = data['password']

    if not data or not name or not email or not phone or not password:
        result["result"] = "failed"
        result["reason"] = "One or more fields are empty."
        return jsonify(result), 500

    print(f"\nUpdating volunteer with email {email}...\n")

    volunteer = Volunteer.query.filter_by(email = email).first()

    if not volunteer:
        result["result"] = "failed"
        result["reason"] = "User does not exist."
        return jsonify(result), 500

    volunteer.name = name
    volunteer.email = email
    volunteer.phone = phone
    volunteer.password = password
    db.session.commit()

    result["result"] = "success"
    result["user"] = volunteer.get_json()
    return jsonify(result),200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5300, debug=True)
