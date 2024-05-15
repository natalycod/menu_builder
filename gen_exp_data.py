import json


def read_data(filename):
    f = open(filename)
    js = json.load(f)
    f.close()
    return js

def convert_recipe_to_str(recipe, type):
    result = type + ' ' + recipe['recipe_id'] + ' '
    result += recipe['serving_sizes']['serving']['calories'] + ' '
    result += recipe['serving_sizes']['serving']['carbohydrate'] + ' '
    result += recipe['serving_sizes']['serving']['fat'] + ' '
    result += recipe['serving_sizes']['serving']['protein'] + '\n'
    
    for ingr in recipe['ingredients']['ingredient']:
        result += ingr['food_id'] + ' '
    result += '\n'
    return result

def write_recipes_one_type(filename_in, filename_out, type):
    recipes = read_data(filename_in)
    f = open(filename_out, 'w')
    for recipe in recipes:
        s = convert_recipe_to_str(recipe, type)
        f.write(s)
    f.close()

write_recipes_one_type('db_data/breakfast_full.json', 'experiments/breakfast.txt', 'breakfast')
write_recipes_one_type('db_data/lunch_full.json', 'experiments/lunch.txt', 'lunch')
write_recipes_one_type('db_data/dinner_full.json', 'experiments/dinner.txt', 'dinner')
