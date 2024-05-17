import json

import utils.db_utils as db_utils

import utils.yaml_schema_parser as yaml_schema_parser


def main(params):
    menu = db_utils.get_menu(params['menu_id'])

    for i in range(len(menu.recipes)):
        extra_data = db_utils.get_recipe_by_id(menu.recipes[i].recipe_id)
        menu.recipes[i].recipe_url = extra_data.recipe_url
        menu.recipes[i].recipe_name = extra_data.recipe_name
        menu.recipes[i].ingredients = extra_data.ingredients

    return yaml_schema_parser.parse_json_to_handler_response(menu.to_json(), '/get_menu', 'get')
