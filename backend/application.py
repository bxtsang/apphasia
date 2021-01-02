from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import os
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbURL')
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@localhost:3306/aphasia"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

validChoices = ["intern", "volunteer", "core", ""]

# request.args: the key/value pairs in the URL query string
# request.form: the key/value pairs in the body, from a HTML post form, or JavaScript request that isn't JSON encoded
# request.files: the files in the body, which Flask keeps separate from form. HTML forms must use enctype=multipart/form-data or files will not be uploaded.
# request.values: combined args and form, preferring args if keys overlap
# request.json: parsed JSON data. The request must have the application/json content type, or use request.get_json(force=True) to ignore the content type.
# All of these are MultiDict instances (except for json). You can access values using:

# request.form['name']: use indexing if you know the key exists
# request.form.get('name'): use get if the key might not exist
# request.form.getlist('name'): use getlist if the key is sent multiple times and you want a list of values. get only returns the first value.

class User(db.Model):
    __tablename__ = "user"

    userID = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.Integer())
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(128), nullable =False)

    def get_json(self):
        return {'userID': self.userID, 'name': self.name, 'email': self.email, 'phone': self.phone, 'password': self.password, 'role': self.role}

@app.route("/user/<userID>", methods=["GET"])
def getUser(userID):
    result = {}

    user = User.query.filter_by(userID = userID).first()

    print(f"\nRetrieving data for user team member with userID: {userID}...\n")

    if not user:
        result["result"] = "Failed"
        result["message"] = "No such user exists"
        return jsonify(result), 500

    result["result"] = "success"
    result["user"] = user.get_json()

    return jsonify(result)

@app.route("/user", methods=["GET"])
def getAllUser():
    userList = []
    result = {}
    data = request.get_json()

    if "role" not in data or data["role"].strip(" ") == "":
        role = ""
    else:
        role = data['role']

    role = role.lower()

    if role not in validChoices:
        result['result'] = "Failed"
        result['message'] = "Invalid role"
        return jsonify(result), 500

    if role != "":
        users = User.query.filter_by(role=role).all()
    else:
        users = User.query.all()

    print(f"\nReturning all users data...\n")

    for user in users:
        userList.append(user.get_json())

    result['result'] = "success"
    result['users'] = userList

    return jsonify(result), 200

@app.route("/user", methods=["POST"])
def addUser():
    result = {}
    data = request.get_json()
    name = data['name']
    email = data['email']
    phone = data['phone']
    password = data['password']
    role = data['role']

    if role == "":
        result['result'] = "Failed"
        result['message'] = "Role required"
        return jsonify(result), 500

    if role not in validChoices:
        result['result'] = "Failed"
        result['message'] = "Invalid role"
        return jsonify(result), 500

    if not data or not name or not email or not phone or not password or not role:
        result["result"] = "Failed"
        result["message"] = "One or more fields are empty."
        return jsonify(result), 500

    user = User(name = name, email = email, phone = phone, password = password, role=role)

    print(f"\nAdding new user member {name}...\n")

    db.session.add(user)
    db.session.commit()

    result["result"] = "success"
    result["user"] = user.get_json()
    return jsonify(result), 200

@app.route("/user", methods=["DELETE"])
def removeUser():
    result = {}
    data = request.get_json()
    userID = data['userID']

    if not userID:
        result["result"] = "Failed"
        result["message"] = "UserID field is empty."
        return jsonify(result), 500

    user = User.query.filter_by(userID= userID).first()

    print(f"\nDeleteing user member with userID: {userID}...\n")

    if not user:
        result["result"] = "Failed"
        result["message"] = "User cannot be found."
        return jsonify(result), 500

    User.query.filter_by(userID = userID).delete()
    db.session.commit()
    
    result["result"] = "success"
    return jsonify(result),200

@app.route("/user", methods=["PUT"])
def updateUser():
    result = {}
    data = request.get_json()
    name = data['name']
    email = data['email']
    phone = data['phone']
    password = data['password']
    role = data['role']
    newEmail = data['newEmail']

    if not data or not name or not email or not phone or not password or not role:
        result["result"] = "Failed"
        result["message"] = "One or more fields are empty."
        return jsonify(result), 500

    print(f"\nUpdating user member with email {email}...\n")

    user = User.query.filter_by(email = email).first()

    if not user:
        result["result"] = "Failed"
        return jsonify(result), 500

    user.name = name
    user.email = newEmail
    user.phone = phone
    user.password = password
    user.role = role
    db.session.commit()

    result["result"] = "success"
    result["user"] = user.get_json()
    return jsonify(result),200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5300, debug=True)
