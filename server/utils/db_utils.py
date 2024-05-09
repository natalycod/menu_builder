import json
import random
import sqlite3

from sqlite3 import Error

from utils.data_classes import Recipe, Menu, Ingredient, Nutrition

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

def save_menu(menu : Menu, menues_path : str = MENUES_PATH):
    connection = create_connection(menues_path)
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
        dinner_info TEXT NOT NULL
    );''')
    connection.commit()

    recipes = []
    for recipe in menu.recipes:
        recipes.append({
            'recipe_id': recipe.recipe_id,
            'calories': recipe.nutrition.calories,
        })

    cursor.execute('INSERT INTO Menues (id, calories, carbohydrates, fats, proteins, breakfast_info, lunch_info, dinner_info) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (menu.id, menu.nutrition.calories, menu.nutrition.carbohydrates, menu.nutrition.fats, menu.nutrition.proteins, json.dumps(recipes[0]), json.dumps(recipes[1]), json.dumps(recipes[2])))
    connection.commit()

    connection.close()

def get_menu(menu_id: str, menues_path : str = MENUES_PATH) -> Menu:
    connection = create_connection(menues_path)
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM Menues WHERE id="{menu_id}"')
    menues = cursor.fetchall()
    for menu in menues:
        result = Menu()
        result.id = menu_id
        result.nutrition = Nutrition(menu[1], menu[2], menu[3], menu[4])

        breakfast_recipe = get_recipe_by_id(json.loads(menu[5])['recipe_id'])
        breakfast_recipe = breakfast_recipe * (json.loads(menu[5])['calories'] / breakfast_recipe.nutrition.calories)
        lunch_recipe = get_recipe_by_id(json.loads(menu[6])['recipe_id'])
        lunch_recipe = lunch_recipe * (json.loads(menu[6])['calories'] / lunch_recipe.nutrition.calories)
        dinner_recipe = get_recipe_by_id(json.loads(menu[7])['recipe_id'])
        dinner_recipe = dinner_recipe * (json.loads(menu[7])['calories'] / dinner_recipe.nutrition.calories)
        
        result.recipes = [breakfast_recipe, lunch_recipe, dinner_recipe]
        return result
    connection.close()

def get_random_recipes(type: str, amount: int, recipes_path : str = RECIPES_PATH):
    connection = create_connection(recipes_path)
    cursor = connection.cursor()
    cursor.execute(f'SELECT recipe_id, calories, carbohydrates, fats, proteins, url, image_url, name, ingredients, instructions FROM Recipes WHERE recipe_type="{type}"')

    result = []
    recipes = cursor.fetchall()
    random.shuffle(recipes)
    recipes = recipes[:amount]

    for recipe in recipes:
        ingredients = []
        for ingr in json.loads(recipe[8]):
            ingredients.append(Ingredient(id=ingr['id'], unit=ingr['unit'], unit_amount=ingr['unit_amount']))
        nutrition = Nutrition(recipe[1], recipe[2], recipe[3], recipe[4])
        recipe = Recipe(recipe_id=recipe[0], nutrition=nutrition, recipe_url=recipe[5], image_url=recipe[6], recipe_name=recipe[7], ingredients=ingredients, instructions=json.loads(recipe[9]))
        result.append(recipe)
    return result

def get_recipe_by_id(recipe_id : str, recipes_path : str = RECIPES_PATH):
    connection = create_connection(recipes_path)
    cursor = connection.cursor()
    cursor.execute(f'SELECT recipe_id, calories, carbohydrates, fats, proteins, url, image_url, name, ingredients, instructions FROM Recipes WHERE recipe_id="{recipe_id}"')

    recipes = cursor.fetchall()

    for recipe in recipes:
        ingredients = []
        for ingr in json.loads(recipe[8]):
            ingredient = get_ingredient_by_id(ingr['id'], ingr['unit']) * ingr['unit_amount']
            ingredients.append(ingredient)
        nutrition = Nutrition(recipe[1], recipe[2], recipe[3], recipe[4])
        recipe = Recipe(recipe_id=recipe[0], nutrition=nutrition, recipe_url=recipe[5], image_url=recipe[6], recipe_name=recipe[7], ingredients=ingredients, instructions=json.loads(recipe[9]))
        return recipe
    return None

def get_ingredient_by_id(ingredient_id : str, unit : str = None, ingredients_path : str = INGREDIENTS_PATH):
    connection = create_connection(ingredients_path)
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM Ingredients WHERE id="{ingredient_id}"')

    ingredients = cursor.fetchall()

    if unit == 'g':
        for ingr in ingredients:
            nutrition = Nutrition(ingr[3], ingr[4], ingr[5], ingr[6])
            return Ingredient(ingr[0], ingr[1], ingr[2], nutrition, 'g', 1)

    if unit == 'ml':
        for ingr in ingredients:
            nutrition = Nutrition(ingr[7], ingr[8], ingr[9], ingr[10])
            return Ingredient(ingr[0], ingr[1], ingr[2], nutrition, 'ml', 1)

    for ingr in ingredients:
        if ingr[3] is not None:
            nutrition = Nutrition(ingr[3], ingr[4], ingr[5], ingr[6])
            return Ingredient(ingr[0], ingr[1], ingr[2], nutrition, 'g', 1)
        if ingr[7] is not None:
            nutrition = Nutrition(ingr[7], ingr[8], ingr[9], ingr[10])
            return Ingredient(ingr[0], ingr[1], ingr[2], nutrition, 'ml', 1)

    return None

def save_menu_to_calendar(user_id : str, date : str, menu_id : str, calendar_path : str = CALENDAR_PATH):
    connection = create_connection(calendar_path)
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

def delete_menu_from_calendar(user_id : str, date : str, menu_id : str = None, calendar_path : str = CALENDAR_PATH):
    connection = create_connection(calendar_path)
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

def get_menues_from_calendar(user_id : str, date_start: str, date_end : str, calendar_path : str = CALENDAR_PATH):
    datestamp_start = int(date_start[6:10] + date_start[3:5] + date_start[0:2])
    datestamp_end = int(date_end[6:10] + date_end[3:5] + date_end[0:2])
    
    connection = create_connection(calendar_path)
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
