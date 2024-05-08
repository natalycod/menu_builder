import json

import db_utils
import utils.yaml_schema_parser as yaml_schema_parser


def main(args):
    ingrs = {}

    menues = db_utils.get_menues_from_calendar(args['user_id'], args['date_start'], args['date_end'])
    for menu_info in menues:
        menu_id = menu_info[1]
        menu = db_utils.get_menu(menu_id)

        for recipe in menu.recipes:
            recipe_full = db_utils.get_recipe_by_id(recipe.recipe_id)
            mult = recipe.nutrition.calories / float(recipe_full.nutrition.calories)
            for ingr in recipe_full.ingredients:
                if ingr.id in ingrs:
                    ingrs[ingr.id] = ingrs[ingr.id] + ingr
                else:
                    ingrs[ingr.id] = ingr

    result = []
    for key in ingrs.keys():
        ingredient = ingrs[key]
        result.append({
            "name": ingredient.name,
            "id": ingredient.id,
            "url": ingredient.url,
            "unit": ingredient.unit,
            "unit_amount": ingredient.unit_amount,
        })

    return yaml_schema_parser.parse_json_to_handler_response(result, '/calendar/get_grocery_list', 'get')
