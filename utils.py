from constants import TEAMS


def get_greeting_text(name):
    return f'Привет, {name}! Введи название сценария. Хотя бы несколько букв. Если найдётся один сценарий, сможешь поменять его приоритет и срок. А ещё можно посмотреть на все сценарии команды, просто введи её название.'


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


