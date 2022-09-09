from constants import TEAMS


def get_greeting_text(name):
    return f'Привет, {name}! Введи название сценария или команды. Хотя бы несколько букв.'


def make_scenario_info_string(scenarios):
    reply = """"""
    for sc in scenarios:
        deadline = f" • {sc['deadline']}" if sc['deadline'] else ''
        reply += f"*{sc['name']}*\n{sc['priority']}{deadline} • {sc['status']} • {sc['designer']}\n\n"

    return reply


def is_team_name(name):
    for team in TEAMS:
        if len(name) > 2 and name.lower().strip() in team.lower().strip():
            return True


