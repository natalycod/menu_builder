import json
import random
import sqlite3

from sqlite3 import Error

from data_classes import Recipe, Menu, Ingredient
from data_classes import serialize_recipe, deserialize_recipe

INGREDIENTS_PATH = "databases/ingredients.sqlite"
RECIPES_PATH = "databases/recipes.sqlite"
MENUES_PATH = "databases/menues.sqlite"

CALENDAR_PATH = "databases/calendar.sqlite"


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def generate_id() -> str:
    result = ""
    symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    for i in range(30):
        rnd = random.randint(0, len(symbols) - 1)
        result += symbols[rnd]
    return result

def save_menu(menu : Menu):
    connection = create_connection(MENUES_PATH)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Menues (
        id TEXT PRIMARY KEY,
        calories REAL NOT NULL,
        carbohydrates REAL NOT NULL,
        fats REAL NOT NULL,
        proteins REAL NOT NULL,
        breakfast_info TEXT NOT NULL,
        lunch_info TEXT NOT NULL,
        dinner_info TEXT NOT NULL,
        ingredients TEXT NOT NULL
    );''')
    connection.commit()

    cursor.execute('INSERT INTO Menues (id, calories, carbohydrates, fats, proteins, breakfast_info, lunch_info, dinner_info, ingredients) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (menu.id, menu.calories, menu.carbohydrates, menu.fats, menu.proteins, serialize_recipe(menu.recipes[0]), serialize_recipe(menu.recipes[1]), serialize_recipe(menu.recipes[2]), json.dumps([])))
    connection.commit()

    connection.close()

def get_menu(menu_id: str) -> Menu:
    connection = create_connection(MENUES_PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM Menues WHERE id="{menu_id}"')
    menues = cursor.fetchall()
    for menu in menues:
        result = Menu()
        result.id = menu_id
        result.calories = menu[1]
        result.carbohydrates = menu[2]
        result.fats = menu[3]
        result.proteins = menu[4]
        result.recipes = [deserialize_recipe(menu[5]), deserialize_recipe(menu[6]), deserialize_recipe(menu[7])]
        return result
    connection.close()

def get_random_recipes(type: str, amount: int):    
    connection = create_connection(RECIPES_PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT recipe_id, calories, carbohydrates, fats, proteins, url, name, ingredients FROM Recipes WHERE recipe_type="{type}"')

    result = []
    recipes = cursor.fetchall()
    random.shuffle(recipes)
    recipes = recipes[:amount]

    for recipe in recipes:
        ingredients = []
        for ingr in json.loads(recipe[7]):
            ingredients.append(Ingredient(id=ingr['food_id'], name=ingr['food_name'], url=ingr['ingredient_url'], calories=ingr['calories'], carbs=ingr['carbohydrates'], fats=ingr['fats'], prots=ingr['proteins'], unit=ingr['measurement_unit'], unit_amount=ingr['number_of_units']))
        recipe = Recipe(recipe_id=recipe[0], calories=recipe[1], carbs=recipe[2], fats=recipe[3], proteins=recipe[4], recipe_url=recipe[5], recipe_name=recipe[6], ingredients=ingredients)
        result.append(recipe)
    return result

def get_recipe_by_id(recipe_id : str):
    connection = create_connection(RECIPES_PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT recipe_id, calories, carbohydrates, fats, proteins, url, name, ingredients FROM Recipes WHERE recipe_id="{recipe_id}"')

    recipes = cursor.fetchall()

    for recipe in recipes:
        ingredients = []
        for ingr in json.loads(recipe[7]):
            ingredients.append(Ingredient(id=ingr['food_id'], name=ingr['food_name'], url=ingr['ingredient_url'], calories=ingr['calories'], carbs=ingr['carbohydrates'], fats=ingr['fats'], prots=ingr['proteins'], unit=ingr['measurement_unit'], unit_amount=ingr['number_of_units']))
        recipe = Recipe(recipe_id=recipe[0], calories=recipe[1], carbs=recipe[2], fats=recipe[3], proteins=recipe[4], recipe_url=recipe[5], recipe_name=recipe[6], ingredients=ingredients)
        return recipe
    return None

def save_menu_to_calendar(user_id : str, date : str, menu_id : str):
    connection = create_connection(CALENDAR_PATH)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Calendar (
        user_id TEXT NOT NULL,
        date TEXT NOT NULL,
        menu_id TEXT NOT NULL,
        datestamp INT NOT NULL
    );''')
    connection.commit()

    # dd.mm.yyyy -> yyyymmdd
    datestamp = int(date[6:10] + date[3:5] + date[0:2])

    cursor.execute('INSERT INTO Calendar (user_id, date, menu_id, datestamp) VALUES (?, ?, ?, ?)',
                   (user_id, date, menu_id, datestamp))
    connection.commit()

    connection.close()

def delete_menu_from_calendar(user_id : str, date : str, menu_id : str = None):
    connection = create_connection(CALENDAR_PATH)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Calendar (
        user_id TEXT NOT NULL,
        date TEXT NOT NULL,
        menu_id TEXT NOT NULL,
        datestamp INT NOT NULL
    );''')
    connection.commit()

    # dd.mm.yyyy -> yyyymmdd
    datestamp = int(date[6:10] + date[3:5] + date[0:2])
    
    if menu_id is not None:
        cursor.execute(f'DELETE FROM Calendar WHERE datestamp="{datestamp}" AND menu_id="{menu_id}" AND user_id="{user_id}"')
    else:
        cursor.execute(f'DELETE FROM Calendar WHERE datestamp="{datestamp}" AND user_id="{user_id}"')
    
    connection.commit()

    connection.close()

def get_menues_from_calendar(user_id : str, date_start: str, date_end : str):
    datestamp_start = int(date_start[6:10] + date_start[3:5] + date_start[0:2])
    datestamp_end = int(date_end[6:10] + date_end[3:5] + date_end[0:2])
    
    connection = create_connection(CALENDAR_PATH)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Calendar (
        user_id TEXT NOT NULL,
        date TEXT NOT NULL,
        menu_id TEXT NOT NULL,
        datestamp INT NOT NULL
    );''')
    connection.commit()

    cursor.execute(f'SELECT date, menu_id FROM Calendar WHERE datestamp>={datestamp_start} AND datestamp<={datestamp_end} ORDER BY datestamp')

    response = cursor.fetchall()
    result = []

    for resp in response:
        date = resp[0]
        menu_id = resp[1]
        result.append([date, menu_id])
    return result
