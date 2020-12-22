from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import os
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbURL')
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@localhost:3306/core"
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

class Core(db.Model):
    __tablename__ = "core"

    userID = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.Integer())
    password = db.Column(db.String(128), nullable=False)

    def get_json(self):
        return {'userID': self.userID, 'name': self.name, 'email': self.email, 'phone': self.phone, 'password': self.password}


@app.route("/core/<userID>", methods=["GET"])
def getCore(userID):
    result = {}

    core = Core.query.filter_by(userID = userID).first()

    print(f"\nRetrieving data for core team member with userID: {userID}...\n")

    if not core:
        result["result"] = "failed"
        result["reason"] = "No such user exists"
        return jsonify(result), 500

    result["result"] = "success"
    result["user"] = core.get_json()

    return jsonify(result)

@app.route("/core", methods=["GET"])
def getAllCore():
    cores = Core.query.all()
    coreList = []
    result = {}

    print(f"\nReturning all core members data...\n")

    for core in cores:
        coreList.append(core.get_json())

    result['result'] = "success"
    result['users'] = coreList

    return jsonify(result), 200

@app.route("/core", methods=["POST"])
def addCore():
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

    core = Core(name = name, email = email, phone = phone, password = password)

    print(f"\nAdding new core member {name}...\n")

    db.session.add(core)
    db.session.commit()

    result["result"] = "success"
    result["user"] = core.get_json()
    return jsonify(result), 200

@app.route("/core", methods=["DELETE"])
def removeCore():
    result = {}
    data = request.get_json()
    email = data['email']

    if not email:
        result["result"] = "failed"
        result["reason"] = "Email field is empty."
        return jsonify(result), 500

    core = Core.query.filter_by(email = email).first()

    print(f"\nDeleteing core member with email: {email}...\n")

    if not core:
        result["result"] = "failed"
        result["reason"] = "User cannot be found."
        return jsonify(result), 404

    Core.query.filter_by(email = email).delete()

    result["result"] = "success"
    return jsonify(result),200

@app.route("/core", methods=["PUT"])
def updateCore():
    result = {}
    data = request.get_json()
    name = data['name']
    email = data['email']
    phone = data['phone']
    password = data['password']
    newEmail = data['newEmail']
    
    if not data or not name or not email or not phone or not password:
        result["result"] = "failed"
        result["reason"] = "One or more fields are empty."
        return jsonify(result), 500

    print(f"\nUpdating core member with email {email}...\n")

    core = Core.query.filter_by(email = email).first()

    if not core:
        result["result"] = "failed"
        return jsonify(result), 500

    core.name = name
    core.email = newEmail
    core.phone = phone
    core.password = password
    db.session.commit()

    result["result"] = "success"
    result["user"] = core.get_json()
    return jsonify(result),200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5300, debug=True)
