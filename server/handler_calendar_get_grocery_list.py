import db_utils
import json

from data_classes import serialize_recipe, serialize_menu_to_json

def main(args):
    ingrs = {}

    menues = db_utils.get_menues_from_calendar(args['user_id'], args['date_start'], args['date_end'])
    for menu_info in menues:
        menu_id = menu_info[1]
        menu = db_utils.get_menu(menu_id)

        for recipe in menu.recipes:
            recipe_full = db_utils.get_recipe_by_id(recipe.recipe_id)
            mult = recipe.calories / float(recipe_full.calories)
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

    return result
