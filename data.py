import json

import gspread
from utils import is_team_name
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
creds = os.environ.get('NEW_GOOGLE_CREDS')

service_account = gspread.service_account_from_dict(json.loads(creds))
sheet = service_account.open('Scenarios')
worksheet = sheet.worksheet('Sheet1')
users_worksheet = sheet.worksheet('user_activity')



def get_user_ids():
    users = users_worksheet.get_all_records()
    user_ids = []
    for user in users:
        user_ids.append(user['id'])

    return user_ids

def get_column_index_by_name(name, sheet):
    headers = sheet.row_values(1)
    enumerated_headers = list(enumerate(headers))
    enumerated_headers = [tuple_object for tuple_object in enumerated_headers if tuple_object[1]]
    lookup_table = dict(enumerated_headers)
    lookup_table_reversed = {value: key for key, value in lookup_table.items()}
    index = lookup_table_reversed[name] + 1
    return index


def send_update(payload):
    new_value_and_meta = f'{payload["value"]} ({payload["meta"]})'
    scenario_row = worksheet.find(payload['scenario_name'], in_column=get_column_index_by_name('name', worksheet)).row
    target_cell = worksheet.cell(scenario_row, get_column_index_by_name(payload['param_name'], worksheet))
    old_value = f'{target_cell.value}\n' if target_cell.value else ''
    worksheet.update_cell(target_cell.row, target_cell.col, f'{old_value}{new_value_and_meta}')

def send_user_update(id):
    last_visit_date = f"{datetime.now().strftime('%d.%m %H:%M:%S')}"
    user_row = users_worksheet.find(id, in_column=get_column_index_by_name('id', users_worksheet)).row
    last_visit_cell = users_worksheet.cell(user_row, get_column_index_by_name('last_visit', users_worksheet))
    users_worksheet.update_cell(last_visit_cell.row, last_visit_cell.col, f'{last_visit_date}')

def get_scenarios(query):
    scenarios = worksheet.get_all_records()
    matching_scenarios = []
    f_query = query.lower().strip()

    for obj in scenarios:
        if is_team_name(f_query) and f_query in obj['team'].lower().strip():
            matching_scenarios.append(obj)

        else:
            f_sc_name = obj['name'].lower().strip()

            if f_query == f_sc_name:
                matching_scenarios.append(obj)
                break

            elif f_query in f_sc_name:
                matching_scenarios.append(obj)

    return matching_scenarios
