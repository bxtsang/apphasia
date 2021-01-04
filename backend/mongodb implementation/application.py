from flask import Flask, jsonify, request
from passlib.hash import pbkdf2_sha256 
import uuid
import pymongo

app = Flask(__name__)

# Database
client = pymongo.MongoClient('localhost', 27017)
db = client.aphasia

class User:

    def signup(self):

        # Retrieve user data from front end
        data = request.get_json()

        # Create user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": data['name'],
            "email": data['email'],
            "password": data['password'],
            "role": data['role'],
            "phone": data['phone']
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Check for existing email address
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        if db.users.insert_one(user):
            return jsonify(user), 200
        
        return jsonify({"error": "Signup failed"}), 400


# Routes
@app.route('/signup', methods=["POST"])
def signup():
    return User().signup()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5300, debug=True)

