import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("/Users/denis/keys/focusdesignbot-firebase-adminsdk-6vob8-45f374b859.json")

default_app = firebase_admin.initialize_app(cred, {
    "databaseURL": "https://focusdesignbot-default-rtdb.firebaseio.com",
})


def get_scenario_status(name):
    scenarios_dict = db.reference('/scenarios').get()
    for obj in scenarios_dict:
        if obj['name'] == name:
            return obj['status']
