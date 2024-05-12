import json
import requests


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
