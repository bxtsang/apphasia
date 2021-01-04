from passlib.hash import pbkdf2_sha256
import pymongo

client = pymongo.MongoClient("localhost", 27017)
dbList = client.list_database_names()

# Helper method to get object ID
def getId(name, colType):
    if colType == "user":
        collection = db['users']
    
    elif colType == "task":
        collection = db['tasks']

    elif colType == "project":
        collection = db['projects']

    
    elif colType == "resource":
        collection = db['resource']

    return collection.find_one({"name": name}, {"_id": 1})['_id']

# Drop db if it exists 
if "aphasia" in dbList:
    client.drop_database('aphasia')

# Create db and collections
db = client['aphasia']
usersCol = db['users']
projectsCol = db['projects']
tasksCol = db['tasks']
resourceCol = db['resource']

# Create default users data
default_users = [
    {
        "email": "cliffen123@gmail.com",
        "name": "Cliffen Lee Jun Yi",
        "password": "testtest",
        "phone": 69798999,
        "role": "core",
    },
    {
        "email": "glenwaves@gmail.com",
        "name": "Glen See Saw",
        "password": "test32",
        "phone": 99887766,
        "role": "core",
    },
    {
        "email": "marydonut@gmail.com",
        "name": "Mary Had Little Lamb",
        "password": "test324",
        "phone": 98897667,
        "role": "core",
    },
    {
        "email": "englieh@gmail.com",
        "name": "Beng Lieh",
        "password": "kuasimikua78",
        "phone": 94847464,
        "role": "volunteer",
    },
    {
        "email": "hweepink@gmail.com",
        "name": "Hwee Purple",
        "password": "aiuhdsjkfn78",
        "phone": 95857565,
        "role": "volunteer",
    },
    {
        "email": "sunjun@gmail.com",
        "name": "Moon Jun",
        "password": "sakfjklfsa890",
        "phone": 96867664,
        "role": "volunteer",
    },
    {
        "email": "arix@gmail.com",
        "name": "Brix Phua",
        "password": "asiodfhiuyesa2",
        "phone": 91817161,
        "role": "intern",
    },
    {
        "email": "baoxian@gmail.com",
        "name": "Bao Xi",
        "password": "981237kjhsdf",
        "phone": 92827262,
        "role": "intern",
    },
    {
        "email": "eunice@gmail.com",
        "name": "Smaen Mae",
        "password": "Hellaosdi23",
        "phone": 90872712,
        "role": "intern",
    },
    {
        "email": "yeowShort@gmail.com",
        "name": "Yeow Leong Chiccen Rice",
        "password": "safasdf1231",
        "phone": 87982871,
        "role": "intern",
    }
]


# Create default tasks data
default_tasks = [
    {
        "name": "Create edm"
    },
    {
        "name": "Submit certificate"
    },
    {
        "name": "Plan budget"
    },
    {
        "name": "Send report"
    },
    {
        "name": "Create timeline for project"
    },
    {
        "name": "Inform interns"
    }
]

# Create default resource data
default_resource = [
    {
        "name": "edm.png"
    },
    {
        "name": "cert.jpg"
    },
    {
        "name": "applePie.png"
    }
]

# Populate data
for user in default_users:
    user['password'] = pbkdf2_sha256.hash(user['password'])
    db.users.insert_one(user)
    db.users.create_index("email", unique = True)

for task in default_tasks:
    db.tasks.insert_one(task)

for resource in default_resource:
    db.resource.insert_one(resource)

# Create default projects data
default_projects = [
    {
        "name": "Wa meng ti",
        "description": "Singing with them peeps",
        "assigned": [getId("Bao Xi", "user"), 
            getId("Brix Phua", "user"),
            getId("Mary Had Little Lamb", "user"), 
            getId("Smaen Mae", "user")],
        "recurring": True,
        "recurring_date": [1,4,5],
        "start_date": "2020-03-25",
        "end_date": "2020-06-17",
        "archived": False,
        "tasks": [getId("Create timeline for project", "task"), 
            getId("Submit certificate", "task")]
    },
        {
        "name": "Night night",
        "description": "Reading with them peeps",
        "assigned": [getId("Hwee Purple", "user"), 
            getId("Moon Jun", "user")],
        "recurring": False, 
        "start_date": "2019-12-11",
        "end_date": "2020-02-12",
        "archived": False,
        "tasks":  [getId("Plan budget", "task"), 
            getId("Inform interns", "task")]
    },
        {
        "name": "Zoomba",
        "description": "Dancing with them peeps, online",
        "assigned": [getId("Cliffen Lee Jun Yi", "user"), 
            getId("Glen See Saw", "user")],
        "recurring": True,
        "recurring_date": [0,1,4,5,6],
        "start_date": "2020-01-01",
        "end_date": "2020-12-30",
        "archived": False,
        "tasks": [getId("Create edm", "task"), 
            getId("Send report", "task")]
    }
]

# Populate projects data
for project in default_projects:
    db.projects.insert_one(project)





