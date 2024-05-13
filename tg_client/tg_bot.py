import requests
import json

token = "TG_BOT_TOKEN"

server_url = "http://127.0.0.1:5000"

MAX_OFFSET = 1

def float_to_str(x : float, precision : int) -> str:
    res = int(x * (10**precision)) / 10**precision
    return str(res)

def build_menu_command(args):
    calories = []
    for x in args:
        calories.append(float(x))
    response = requests.post(server_url + "/build_menu", json = {"calories": calories})
    menu = json.loads(response.text)

    message = "menu_id: " + menu["menu_id"] + "\n"
    message += "total calories: " + float_to_str(menu["nutrition"]["calories"], 2) + "\n"
    message += "(" + float_to_str(menu["nutrition"]["carbohydrates"], 2) + ", " + float_to_str(menu["nutrition"]["fats"], 2) + ", " + float_to_str(menu["nutrition"]["proteins"], 2) + ")" + "\n"
    message += "\n"
    message += "Breakfast: " + menu["breakfast_info"]["recipe_name"] + "\n"
    message += "Lunch: " + menu["lunch_info"]["recipe_name"] + "\n"
    message += "Dinner: " + menu["dinner_info"]["recipe_name"] + "\n"

    return message

def save_menu_command(args, user_id):
    if len(args) != 2:
        return "Need 2 arguments for /save_menu command"
    response = requests.post(server_url + "/calendar/save_menu", json = {"user_id": "tg_" + user_id, "menu_id": args[0], "date": args[1]})

    if response.status_code // 100 == 2:
        return "Successfully saved menu"
    else:
        return "Couldn't save menu, try again later"

def get_menu_by_id(args):
    if len(args) != 1:
        return "Need 1 argument for /get_menu_by_id command"

    url = server_url + "/get_menu?menu_id=" + args[0]
    response = requests.get(url)
    menu = json.loads(response.text)

    message = "menu_id: " + menu["menu_id"] + "\n"
    message += "total calories: " + float_to_str(menu["nutrition"]["calories"], 2) + "\n"
    message += "(" + float_to_str(menu["nutrition"]["carbohydrates"], 2) + ", " + float_to_str(menu["nutrition"]["fats"], 2) + ", " + float_to_str(menu["nutrition"]["proteins"], 2) + ")" + "\n"
    message += "\n"
    message += "Breakfast: " + menu["breakfast_info"]["recipe_name"] + "\n"
    message += "Lunch: " + menu["lunch_info"]["recipe_name"] + "\n"
    message += "Dinner: " + menu["dinner_info"]["recipe_name"] + "\n"

    return message

def get_menu_by_date(args, user_id):
    if len(args) != 1:
        return "Need 1 argument for /get_menu_by_date command"

    url = server_url + "/calendar/get_menues?user_id=tg_" + user_id + "&date_start=" + args[0] + "&date_end=" + args[0]
    response = requests.get(url)

    menues = json.loads(response.text)
    if len(menues) == 0:
        return "Couldn't find any menu for those dates"

    message = ""
    for menu_info in menues:
        message += "Date: " + menu_info["date"] + "\n"
        message += "Menu_id: " + menu_info["menu"]["menu_id"] + "\n"
        message += "Breakfast: " + menu_info["menu"]["meals"][0] + "\n"
        message += "Lunch: " + menu_info["menu"]["meals"][1] + "\n"
        message += "Dinner: " + menu_info["menu"]["meals"][2] + "\n"
        message += "\n"

    return message

def get_menues_by_dates(args, user_id):
    if len(args) != 2:
        return "Need 2 arguments for /get_menu_by_date command"

    url = server_url + "/calendar/get_menues?user_id=tg_" + user_id + "&date_start=" + args[0] + "&date_end=" + args[1]
    response = requests.get(url)

    menues = json.loads(response.text)
    if len(menues) == 0:
        return "Couldn't find any menu for those dates"

    message = ""
    for menu_info in menues:
        message += "Date: " + menu_info["date"] + "\n"
        message += "Menu_id: " + menu_info["menu"]["menu_id"] + "\n"
        message += "Breakfast: " + menu_info["menu"]["meals"][0] + "\n"
        message += "Lunch: " + menu_info["menu"]["meals"][1] + "\n"
        message += "Dinner: " + menu_info["menu"]["meals"][2] + "\n"
        message += "\n"

    return message

def get_grocery_list(args, user_id):
    if len(args) != 2:
        return "Need 2 arguments for /get_grocery_list command"

    url = server_url + "/calendar/get_grocery_list?user_id=tg_" + user_id + "&date_start=" + args[0] + "&date_end=" + args[1]
    response = requests.get(url)

    grocery_list = json.loads(response.text)

    message = ""
    for food in grocery_list:
        message += food["name"] + ": " + float_to_str(food["unit_amount"], 2) + " " + food["unit"] + "\n"

    return message


def answering_to_message(message_info):
    try:
        global MAX_OFFSET
        js = message_info

        user_id = str(js["message"]["from"]["id"])
        mess = str(js["message"]["text"])
        mess_id = int(js["update_id"])

        answer = "Sorry, couldn't parse this command"

        arr = mess.split(" ")
        command = arr[0]
        args = arr[1:]
        if command == "/build_menu":
            answer = build_menu_command(args)
        if command == "/save_menu":
            answer = save_menu_command(args, user_id)
        if command == "/get_menu_by_id":
            answer = get_menu_by_id(args)
        if command == "/get_menu_by_date":
            answer = get_menu_by_date(args, user_id)
        if command == "/get_menues_by_dates":
            answer = get_menues_by_dates(args, user_id)
        if command == "/get_grocery_list":
            answer = get_grocery_list(args, user_id)

        response = requests.get("https://api.telegram.org/bot" + token + "/sendMessage?chat_id=" + user_id + "&text=" + answer)

        MAX_OFFSET = max(MAX_OFFSET, mess_id + 1)
    except:
        pass

while True:
    response = requests.get("https://api.telegram.org/bot" + token + "/getUpdates?offset=" + str(MAX_OFFSET))
    for message in json.loads(response.text)["result"]:
        answering_to_message(message)
