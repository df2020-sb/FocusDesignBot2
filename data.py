import gspread
from utils import is_team_name

service_account = gspread.service_account()
sheet = service_account.open('Scenarios')
worksheet = sheet.worksheet('Sheet1')


def get_column_index_by_name(name):
    headers = worksheet.row_values(1)
    enumerated_headers = list(enumerate(headers))
    enumerated_headers = [tuple_object for tuple_object in enumerated_headers if tuple_object[1]]
    lookup_table = dict(enumerated_headers)
    lookup_table_reversed = {value: key for key, value in lookup_table.items()}
    index = lookup_table_reversed[name] + 1
    return index


def send_update(payload):
    new_value_and_meta = f'{payload["value"]} ({payload["meta"]})'
    scenario_row = worksheet.find(payload['scenario_name'], in_column=get_column_index_by_name('name')).row
    target_cell = worksheet.cell(scenario_row, get_column_index_by_name(payload['param_name']))
    old_value = f'{target_cell.value}\n' if target_cell.value else ''
    worksheet.update_cell(target_cell.row, target_cell.col, f'{old_value}{new_value_and_meta}')


def get_scenarios(query):
    scenarios = worksheet.get_all_records()
    matching_scenarios = []

    for obj in scenarios:
        f_query = query.lower().strip()
        query_test = obj['team'].lower().strip() if is_team_name(f_query) else obj['name'].lower().strip()

        if f_query in query_test:
            matching_scenarios.append(obj)

    return matching_scenarios
