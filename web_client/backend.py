import datetime
import json
import requests
import time


server_url = "http://127.0.0.1:6000"

def backend_build_menu(args, menu_prev, calories):
    req = {
        "calories": [calories]
    }
    if 'breakfast_fixed' in args and args['breakfast_fixed'] == 'true':
        req['breakfast_id'] = menu_prev['breakfast_info']['recipe_id']
    if 'lunch_fixed' in args and args['lunch_fixed'] == 'true':
        req['lunch_id'] = menu_prev['lunch_info']['recipe_id']
    if 'dinner_fixed' in args and args['dinner_fixed'] == 'true':
        req['dinner_id'] = menu_prev['dinner_info']['recipe_id']
    
    print("natalycod_debug: request = ", req)
    response = requests.post(server_url + "/build_menu", json=req)
    return json.loads(response.text)

def backend_get_menu(menu_id):
    url = server_url + "/get_menu?menu_id=" + menu_id
    response = requests.get(url)
    return json.loads(response.text)

def backend_menu_get_grocery_list(menu_id):
    url = server_url + "/menu/get_grocery_list?menu_id=" + menu_id
    response = requests.get(url)
    return json.loads(response.text)

def backend_calendar_save_menu(user_id, date, menu_id):
    url = server_url + "/calendar/save_menu"
    response = requests.post(url, json={
        'user_id': user_id,
        'menu_id': menu_id,
        'date': date,
    })

def backend_calendar_delete_menu(user_id, date):
    url = server_url + "/calendar/delete_menu"
    response = requests.post(url, json={
        'user_id': user_id,
        'date': date,
    })

def backend_calendar_get_menues(user_id, date_start, date_end):
    url = server_url + "/calendar/get_menues?user_id=" + user_id + "&date_start=" + date_start + "&date_end=" + date_end
    response = requests.get(url)
    return json.loads(response.text)

def convert_date_to_string(day : int, month : int, year: int) -> str:
    day_s = str(day)
    month_s = str(month)
    year_s = str(year)
    while len(day_s) < 2:
        day_s = "0" + day_s
    while len(month_s) < 2:
        month_s = "0" + month_s
    while len(year_s) < 4:
        year_s = "0" + year_s
    return day_s + "." + month_s + "." + year_s

def get_today_date():
    date_today = datetime.date.today()
    return convert_date_to_string(date_today.day, date_today.month, date_today.year)

def is_vis_year(year : int):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0

def get_previous_date(date : str):
    props = date.split('.')
    day = int(props[0])
    month = int(props[1])
    year = int(props[2])

    days_amount = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_vis_year(year):
        days_amount[2] = 29

    if day != 1:
        return convert_date_to_string(day - 1, month, year)
    if month != 1:
        return convert_date_to_string(days_amount[month - 1], month - 1, year)
    return convert_date_to_string(31, 12, year - 1)

def get_next_date(date : str):
    props = date.split('.')
    day = int(props[0])
    month = int(props[1])
    year = int(props[2])

    days_amount = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_vis_year(year):
        days_amount[2] = 29

    if day != days_amount[month]:
        return convert_date_to_string(day + 1, month, year)
    if month != 12:
        return convert_date_to_string(1, month + 1, year)
    return convert_date_to_string(1, 1, year + 1)
