import json
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd
from pandas import DataFrame

load_dotenv()

cred = credentials.Certificate(json.loads(os.environ.get('GOOGLE_CREDS')))

default_app = firebase_admin.initialize_app(cred, {
    "databaseURL": "https://focusdesignbot-default-rtdb.firebaseio.com",
})


# def get_scenario_status(name):
#     scenarios_dict = db.reference('/scenarios').get()
#     for obj in scenarios_dict:
#         if obj['name'] == name:
#             return obj['status']
#
#
# current_data = []
#
#
# def handle_event(event):
#     global current_data
#     new_data = list(filter(None, event.data))
#     for obj in new_data:
#         if obj not in current_data:
#             print(obj['name'], obj['status'])
#
#     current_data = event.data


# def compare_two_lists(list1, list2):
#     df1 = pd.DataFrame(list1)
#     df2 = pd.DataFrame(list2)
#     diff = DataFrame.diff(df1, df2)
#     result = len(diff) == 0
#     if not result:
#         print(f'There are {len(diff)} differences:\n{diff.head()}')
#     return result

# db.reference('/').child('scenarios').listen(handle_event)
