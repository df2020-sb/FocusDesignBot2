from constants import TEAMS

def getGreetingText(name):
    return f'Привет, {name}! Введи название сценария или команды'

def make_scenario_info_string(sc):
    # return f"*{sc['name'].title()}*\n{sc['priority']} • {sc['date']} • {sc['status']} • {sc['designer']} \n\n"
    return f"<b>{sc['name'].title()}</b>\n{sc['priority']} • {sc['date']} • {sc['status']} • {sc['designer']}\n\n"


def is_team_name(name):
    for team in TEAMS:
        if name.lower().strip() in team:
            return True
