import json
import random
import sqlite3

from sqlite3 import Error

INGREDIENTS_PATH = "server/databases/ingredients.sqlite"

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def save_ingredient(js, nutrition_per_g, nutrition_per_ml):
    connection = create_connection(INGREDIENTS_PATH)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ingredients (
        id INT PRIMARY KEY,
        name TEXT NOT NULL,
        url TEXT,
        calories_per_g REAL,
        carbohydrates_per_g REAL,
        fats_per_g REAL,
        proteins_per_g REAL,
        calories_per_ml REAL,
        carbohydrates_per_ml REAL,
        fats_per_ml REAL,
        proteins_per_ml REAL
    );''')
    connection.commit()

    cursor.execute('INSERT INTO Ingredients (id, name, url, calories_per_g, carbohydrates_per_g, fats_per_g, proteins_per_g, calories_per_ml, carbohydrates_per_ml, fats_per_ml, proteins_per_ml) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (js['food_id'], js['food_name'], js['food_url'],
                    nutrition_per_g['calories'], nutrition_per_g['carbs'], nutrition_per_g['fats'], nutrition_per_g['prots'],
                    nutrition_per_ml['calories'], nutrition_per_ml['carbs'], nutrition_per_ml['fats'], nutrition_per_ml['prots']))
    connection.commit()

    connection.close()

s = set()

for type in ["breakfast", "lunch", "dinner"]:
    f = open("db/" + type + "_full.json")
    js = json.load(f)
    f.close()

    for recipe in js:
        ingredients_temp = []
        try:
            recipe['ingredients']['ingredient'][0]
            ingredients_temp = recipe['ingredients']['ingredient']
        except:
            ingredients_temp = [recipe['ingredients']['ingredient']]
        for ingredient_temp in ingredients_temp:
            s.add(ingredient_temp['food_id'])

def get_nutrition_per_g(ingr):
    servings = []
    try:
        ingr['servings']['serving'][0]
        servings = ingr['servings']['serving']
    except:
        servings = [ingr['servings']['serving']]
    for serving in servings:
        if serving['measurement_description'] == 'g':
            return {
                'calories': float(serving['calories']) / float(serving['number_of_units']),
                'carbs': float(serving['carbohydrate']) / float(serving['number_of_units']),
                'fats': float(serving['fat']) / float(serving['number_of_units']),
                'prots': float(serving['protein']) / float(serving['number_of_units']),
            }

    for serving in servings:
        if serving['measurement_description'] == 'oz':
            return {
                'calories': float(serving['calories']) / float(serving['number_of_units']) / 28.35,
                'carbs': float(serving['carbohydrate']) / float(serving['number_of_units']) / 28.35,
                'fats': float(serving['fat']) / float(serving['number_of_units']) / 28.35,
                'prots': float(serving['protein']) / float(serving['number_of_units']) / 28.35,
            }

    for serving in servings:
        if serving['metric_serving_unit'] == 'g':
            return {
                'calories': float(serving['calories']) / float(serving['metric_serving_amount']),
                'carbs': float(serving['carbohydrate']) / float(serving['metric_serving_amount']),
                'fats': float(serving['fat']) / float(serving['metric_serving_amount']),
                'prots': float(serving['protein']) / float(serving['metric_serving_amount']),
            }

    for serving in servings:
        if serving['metric_serving_unit'] == 'oz':
            return {
                'calories': float(serving['calories']) / float(serving['metric_serving_amount']) / 28.35,
                'carbs': float(serving['carbohydrate']) / float(serving['metric_serving_amount']) / 28.35,
                'fats': float(serving['fat']) / float(serving['metric_serving_amount']) / 28.35,
                'prots': float(serving['protein']) / float(serving['metric_serving_amount']) / 28.35,
            }

    return {
        'calories': None,
        'carbs': None,
        'fats': None,
        'prots': None,
    }

def get_nutrition_per_ml(ingr):
    servings = []
    try:
        ingr['servings']['serving'][0]
        servings = ingr['servings']['serving']
    except:
        servings = [ingr['servings']['serving']]
    for serving in servings:
        if serving['measurement_description'] == 'ml':
            return {
                'calories': float(serving['calories']) / float(serving['number_of_units']),
                'carbs': float(serving['carbohydrate']) / float(serving['number_of_units']),
                'fats': float(serving['fat']) / float(serving['number_of_units']),
                'prots': float(serving['protein']) / float(serving['number_of_units']),
            }

    for serving in servings:
        if serving['metric_serving_unit'] == 'ml':
            return {
                'calories': float(serving['calories']) / float(serving['metric_serving_amount']),
                'carbs': float(serving['carbohydrate']) / float(serving['metric_serving_amount']),
                'fats': float(serving['fat']) / float(serving['metric_serving_amount']),
                'prots': float(serving['protein']) / float(serving['metric_serving_amount']),
            }

    return {
        'calories': None,
        'carbs': None,
        'fats': None,
        'prots': None,
    }

print(len(s))

f = open("db/ingredients.json")
js = json.load(f)
f.close()

for ingr in js:
    if ingr['food_id'] in s:
        nutrition_per_g = get_nutrition_per_g(ingr)
        nutrition_per_ml = get_nutrition_per_ml(ingr)
        save_ingredient(ingr, nutrition_per_g, nutrition_per_ml)
