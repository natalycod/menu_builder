import json

import db_utils
from data_classes import serialize_menu_to_json



def main(params):
    menu = db_utils.get_menu(params['menu_id'])

    for i in range(len(menu.recipes)):
        extra_data = db_utils.get_recipe_by_id(menu.recipes[i].recipe_id)
        menu.recipes[i].recipe_url = extra_data.recipe_url
        menu.recipes[i].recipe_name = extra_data.recipe_name
        # menu.recipes[i].ingredients = extra_data.ingredients

    return serialize_menu_to_json(menu)
