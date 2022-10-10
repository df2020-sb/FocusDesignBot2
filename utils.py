from constants import TEAMS


def get_greeting_text(name):
    return f'Привет, {name}!\nВведи название сценария. Хотя бы примерно.\n\nЕсли найдётся только один сценарий, сможешь поменять его приоритет и срок.\n\nА ещё можно посмотреть все сценарии команды, просто введи её название.\n\nЕсли что, вводи /help'


def make_scenario_info_string(scenarios):
    reply = """"""
    for sc in scenarios:
        deadline = f" • {sc['deadline']}" if sc['deadline'] else ''
        name = f"*{sc['name']}*"
        translation = f" / {sc['translation']}\n"
        other_data = f"{sc['priority']}{deadline} • {sc['status']} • {sc['designer']}\n"
        link = f"[Макет в Фигме]({sc['link']})\n\n"
        reply += f"{name}{translation}{other_data}{link}"

    return reply


def is_team_name(name):
    for team in TEAMS:
        if len(name) > 2 and name.lower().strip() in team.lower().strip():
            return True



