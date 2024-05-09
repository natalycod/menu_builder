import json
import random
import sqlite3

from sqlite3 import Error

RECIPES_PATH = "server/databases/recipes.sqlite"

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def save_recipe(js, type):
    connection = create_connection(RECIPES_PATH)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Recipes (
        id INT PRIMARY KEY,
        recipe_id TEXT NOT NULL,
        recipe_type TEXT NOT NULL,
        name TEXT NOT NULL,
        url TEXT,
        image_url TEXT,
        calories REAL NOT NULL,
        carbohydrates REAL NOT NULL,
        fats REAL NOT NULL,
        proteins REAL NOT NULL,
        ingredients TEXT NOT NULL
    );''')
    connection.commit()

    ingredients = []
    try:
        js['ingredients']['ingredient'][0]
        ingredients = js['ingredients']['ingredient']
    except:
        ingredients = [js['ingredients']['ingredient']]

    for i in range(len(ingredients)):
        ingredients[i] = {
            'id': ingredients[i]['food_id'],
            'unit': ingredients[i]['measurement_unit'],
            'unit_amount': ingredients[i]['number_of_units'] / float(js['number_of_servings'])
        }

    image_url = None
    if 'recipe_images' in js:
        if isinstance(js['recipe_images']['recipe_image'], str):
            image_url = js['recipe_images']['recipe_image']
        else:
            image_url = js['recipe_images']['recipe_image'][0]

    cursor.execute('INSERT INTO Recipes (recipe_id, recipe_type, name, url, image_url, calories, carbohydrates, fats, proteins, ingredients) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (js['recipe_id'], type, js['recipe_name'], js['recipe_url'], image_url,
                    float(js['serving_sizes']['serving']['calories']),
                    float(js['serving_sizes']['serving']['carbohydrate']),
                    float(js['serving_sizes']['serving']['fat']),
                    float(js['serving_sizes']['serving']['protein']),
                    json.dumps(ingredients)))
    connection.commit()

    connection.close()

for type in ["breakfast", "lunch", "dinner"]:
    f = open("db_data/" + type + "_full.json")
    js = json.load(f)
    f.close()

    for recipe in js:
        save_recipe(recipe, type)
