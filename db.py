import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

load_dotenv()

cred = credentials.Certificate({
    "type": "service_account",
    "projectId": os.environ.get('FIREBASE_PROJECT_ID'),
    "private_key": os.environ.get('FIREBASE_PRIVATE_KEY'),
    "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
})

default_app = firebase_admin.initialize_app(cred, {
    "databaseURL": "https://focusdesignbot-default-rtdb.firebaseio.com",
})


def get_scenario_status(name):
    scenarios_dict = db.reference('/scenarios').get()
    for obj in scenarios_dict:
        if obj['name'] == name:
            return obj['status']
