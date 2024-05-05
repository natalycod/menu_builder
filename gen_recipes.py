import json
import random
import sqlite3

from sqlite3 import Error

RECIPES_PATH = "src/databases/recipes.sqlite"

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


    cursor.execute('INSERT INTO Recipes (recipe_id, recipe_type, name, url, calories, carbohydrates, fats, proteins, ingredients) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (js['recipe_id'], type, js['recipe_name'], js['recipe_url'],
                    float(js['serving_sizes']['serving']['calories']) * float(js['number_of_servings']),
                    float(js['serving_sizes']['serving']['carbohydrate']) * float(js['number_of_servings']),
                    float(js['serving_sizes']['serving']['fat']) * float(js['number_of_servings']),
                    float(js['serving_sizes']['serving']['protein']) * float(js['number_of_servings']),
                    json.dumps(ingredients)))
    connection.commit()

    connection.close()

for type in ["breakfast", "lunch", "dinner"]:
    f = open("db/" + type + "_full.json")
    js = json.load(f)
    f.close()

    for recipe in js:
        save_recipe(recipe, type)
