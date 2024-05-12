from flask import Flask, request

import handlers.handler_build_menu as handler_build_menu
import handlers.handler_calendar_delete_menu as handler_calendar_delete_menu
import handlers.handler_calendar_get_grocery_list as handler_calendar_get_grocery_list
import handlers.handler_calendar_get_menues as handler_calendar_get_menues
import handlers.handler_calendar_save_menu as handler_calendar_save_menu
import handlers.handler_get_menu as handler_get_menu


app = Flask("knapsack_app")

@app.route("/build_menu", methods=['POST'])
def build_menu_request():
    return handler_build_menu.main(request.json)

@app.route("/get_menu", methods=['GET'])
def get_menu_request():
    return handler_get_menu.main(request.args)

@app.route("/calendar/save_menu", methods=['POST'])
def calendar_save_menu_request():
    return handler_calendar_save_menu.main(request.json)

@app.route("/calendar/get_menues", methods=['GET'])
def calendar_get_menues_request():
    return handler_calendar_get_menues.main(request.args)

@app.route("/calendar/delete_menu", methods=['POST'])
def calendar_delete_menu_request():
    return handler_calendar_delete_menu.main(request.json)

@app.route("/calendar/get_grocery_list", methods=['GET'])
def calendar_get_grocery_list_request():
    return handler_calendar_get_grocery_list.main(request.args)

app.run(debug=True, port=6000)
