from flask import Flask, jsonify, request, session
from functools import wraps
from passlib.hash import pbkdf2_sha256 
from bson import json_util, ObjectId
import uuid
import pymongo
import json
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "endgame1"

# Database
client = pymongo.MongoClient('localhost', 27017)
db = client.aphasia

class User:

    def start_session(self, user):
        session['id'] = str(user['_id']) 
        return

    def signup(self):

        # Retrieve user data from front end
        data = request.get_json()

        # Create user object
        user = {
            "name": data['name'],
            "email": data['email'],
            "password": data['password'],
            "role": data['role'],
            "phone": data['phone']
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.hash(user['password'])

        # Check for existing email address
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        if db.users.insert_one(user):
            self.start_session(json.loads(json_util.dumps(user)))
            dbUser = db.users.find_one({"email": data['email']})

            return jsonify({"status": True, "user": json.loads(json_util.dumps(dbUser))})
        
        return jsonify({"error": "Signup failed"}), 400

    def signout(self):
        session.clear()

        return jsonify({"status": True, "result": "Session cleared"}) 
    
    def login(self):

        data = request.get_json()

        if data == None or "email" not in data or "password" not in data:
            return jsonify({"status": False, "token": "Email or password not provided"}), 400

        user = db.users.find_one({
            "email": data['email'] 
        })

        
        if user and pbkdf2_sha256.verify(data['password'], user['password']):
            token = jwt.encode({"user": user['name'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            self.start_session(user)
            # user['id'] = str(user['_id'])
            # del user['_id']
            del user['password']
            return jsonify({"status": True, "token": token.decode('UTF-8'), "user": json.loads(json_util.dumps(user))}), 200

        else:
            return jsonify({"status": False, "token" : "Wrong email or password"}), 400

    def me(self):
        user = db.users.find_one({"_id": ObjectId(session['id'])})
        # user['id'] = str(user['_id'])
        # del user['_id']
        del user['password']
        
        return jsonify({"user": json.loads(json_util.dumps(user))}), 200

    def get_all_user(self):
        users = db.users.find()

        return jsonify({"status": True, "result": json.loads(json_util.dumps(users))})


    def get_user(self, userId):
        user = db.users.find_one({"email": ObjectId(userId)})

        return jsonify({"status": True, "result": json.loads(json_util.dumps(user))})

    def update_user(self):
        data = request.get_json()  

        user = db.users.find_one({
            "email": data['current_email'] 
        })

        if user:
            query = {"_id": user['_id']}
            del data['current_email']
            new_values = {"$set" : data}

            if db.users.update_one(query,new_values):
                dbUser = db.users.find_one({"_id": query['_id']})

                return jsonify({"status": True, "user": json.loads(json_util.dumps(dbUser))})
            
            else:
                return jsonify({"status": False, "result": "Update failed"})
        
        else:
            return jsonify({"status": False, "result": "Email is invalid"})

    def delete_user(self):
        data = request.get_json()
        userId = data['_id']
        
        if (db.users.delete_one({"_id": ObjectId(userId)})):
            return jsonify({"status": True, "result": "User deleted successfully"})
        else:
            return jsonify({"status": False, "result": "User deletion failed"})

    def add_user(self):
        data = request.get_json()
        
        # Create user object
        user = {
            "name": data['name'],
            "email": data['email'],
            "password": data['password'],
            "role": data['role'],
            "phone": data['phone']
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.hash(user['password'])

        # Check for existing email address
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        if db.users.insert_one(user):
            self.start_session(json.loads(json_util.dumps(user)))
            dbUser = db.users.find_one({"email": data['email']})

            return jsonify({"status": True, "user": json.loads(json_util.dumps(dbUser))})
        
        return jsonify({"error": "Failed to add user"}), 400

class Project:

    def get_all_project(self):
        projects = db.projects.find()
        project_list = [json.loads(json_util.dumps(project)) for project in projects]
        
        return jsonify({"status": True, "result": project_list}), 200

    def get_project(self, projectId):
        project = db.projects.find_one({"_id": ObjectId(projectId)})
        project = json.loads(json_util.dumps(project))

        return jsonify({"status": True, "result": project}), 200



# Decorators

# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args,**kwargs)
#         else:
#             return "User not logged in", 500

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        if 'token' not in request.headers:
            return jsonify({"status": False, "token": "Token is missing!"}), 401

        token = request.headers['token']
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({"status": False, "token": "Token is invalid"}), 401

        return f(*args, **kwargs)

    return decorated

# Routes
@app.route('/signup', methods=["POST"])
def signup():
    return User().signup()

@app.route('/signout')
def signout():
    return User().signout()

@app.route('/login', methods = ["POST"])
def login():
    return User().login()

@app.route('/me')
@token_required
def me():
    return User().me()

@app.route('/user')
@token_required
def get_all_users():
    return User().get_all_user()

@app.route('/user/<userId>')
@token_required
def get_user(userId):
    return User().get_user(userId)

@app.route('/user', methods = ["PUT"])
@token_required
def update_user():
    return User().update_user()

@app.route('/user', methods = ["DELETE"])
@token_required
def delete_user():
    return User().delete_user()

@app.route('/user', methods = ["POST"])
@token_required
def add_user():
    return User().add_user()
    
@app.route('/projects')
@token_required
def get_all_projects():
    return Project().get_all_project()

@app.route('/projects/<projectId>')
@token_required
def get_project(projectId):
    return Project().get_project(projectId)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5300, debug=True)

