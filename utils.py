from constants import TEAMS


def get_greeting_text(name):
    return f'Привет, {name}!\nВведи название сценария. Хотя бы примерно.\n\nЕсли найдётся только один сценарий, сможешь поменять его приоритет и срок.\n\nА ещё можно посмотреть все сценарии команды, просто введи её название.'


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


