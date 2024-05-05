import db_utils


def main(args):
    menues = db_utils.get_menues_from_calendar(args['user_id'], args['date_start'], args['date_end'])
    result = []
    for menu in menues:
        result.append({
            "date": menu[0],
            "menu": {
                "menu_id": menu[1],
                "meals": []
            },
        })
        menu_full = db_utils.get_menu(menu[1])
        for recipe in menu_full.recipes:
            recipe_full = db_utils.get_recipe_by_id(recipe.recipe_id)
            result[-1]["menu"]["meals"].append(recipe_full.recipe_name)

    return result
