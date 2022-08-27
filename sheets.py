import gspread

from constants import OUT_MESSAGES
from utils import make_scenario_info_string

service_account = gspread.service_account()
sheet = service_account.open('Scenarios')
worksheet = sheet.worksheet('Sheet1')


# for obj in scenarios:
#     if obj['name'] == name:
#         cell = worksheet.find(obj['status'])
#         coordinates = f'R{cell.row}C{cell.col}'
#         worksheet.update(coordinates, 'newstatus')
#
#
#
#


def get_scenario_status(name):
    scenarios = worksheet.get_all_records()
    matching_scenarios = """"""

    for obj in scenarios:
        received_name = name.lower().strip()
        sc_name = obj['name'].lower().strip()

        if received_name in sc_name:
            matching_scenarios += make_scenario_info_string(obj)

    if not matching_scenarios:
        return OUT_MESSAGES['wrong_input']

    return matching_scenarios


def get_team_scenarios(team):
    scenarios = worksheet.get_all_records()
    team_scenarios = """"""
    for obj in scenarios:
        received_team = team.lower().strip()
        sc_team_name = obj['team'].lower().strip()
        if received_team in sc_team_name:
            team_scenarios += make_scenario_info_string(obj)
    return team_scenarios
