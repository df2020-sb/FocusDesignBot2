from constants import TEAMS


def get_greeting_text(name):
    return f'Привет, {name}! Введи название сценария или команды'


def make_scenario_info_string(scenarios):
    reply = """"""
    for sc in scenarios:
        reply += f"*{sc['name'].title()}*\n{sc['priority']} • {sc['deadline']} • {sc['status']} • {sc['designer']}\n\n"

    return reply


def is_team_name(name):
    for team in TEAMS:
        if name.lower().strip() in team:
            return True


