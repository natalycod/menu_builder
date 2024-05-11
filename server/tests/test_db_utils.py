import json
import pytest
import sqlite3
import time

from sqlite3 import Error

import utils.db_utils as db_utils
from utils.data_classes import Menu, Recipe, Ingredient, Nutrition


TEST_INGREDIENTS_PATH = "tests/test_databases/ingredients.sqlite"
TEST_RECIPES_PATH = "tests/test_databases/recipes.sqlite"
TEST_MENUES_PATH = "tests/test_databases/menues.sqlite"
TEST_CALENDAR_PATH = "tests/test_databases/calendar.sqlite"


TEST_RECIPE_1 = Recipe(js={
    'recipe_id': 't_recipe_id_1',
    'name': 't_recipe_name_1',
    'url': 't_recipe_url_1',
    'image_url': 't_recipe_image_url_1',
    'nutrition': {
        'calories': 1000,
        'carbohydrates': 1,
        'fats': 2,
        'proteins': 3,
    },
    'ingredients': [],
    'instructions': ['instruction_1', 'instruction_2', 'instruction_3'],
})

TEST_RECIPE_2 = Recipe(js={
    'recipe_id': 't_recipe_id_2',
    'name': 't_recipe_name_2',
    'url': 't_recipe_url_2',
    'image_url': 't_recipe_image_url_2',
    'nutrition': {
        'calories': 2000,
        'carbohydrates': 4,
        'fats': 5,
        'proteins': 6,
    },
    'ingredients': [],
    'instructions': ['instruction_4', 'instruction_5', 'instruction_6'],
})

TEST_RECIPE_3 = Recipe(js={
    'recipe_id': 't_recipe_id_3',
    'name': 't_recipe_name_3',
    'url': 't_recipe_url_3',
    'image_url': 't_recipe_image_url_3',
    'nutrition': {
        'calories': 3000,
        'carbohydrates': 7,
        'fats': 8,
        'proteins': 9,
    },
    'ingredients': [],
    'instructions': ['instruction_7', 'instruction_8', 'instruction_9'],
})

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def test_save_menu():
    menu = Menu()
    menu.recipes = [TEST_RECIPE_1, TEST_RECIPE_2, TEST_RECIPE_3]
    menu.nutrition = Nutrition(100, 1, 2, 3)
    menu.id = 't_menu_id'

    db_utils.save_menu(menu, TEST_MENUES_PATH)

    connection = create_connection(TEST_MENUES_PATH)
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM Menues')
    menues = cursor.fetchall()
    cursor.execute(f'DROP TABLE Menues')
    connection.commit()
    connection.close()

    assert len(menues) == 1
    
    menu = menues[0]
    assert menu[0] == 't_menu_id'
    assert menu[1] == 100
    assert menu[2] == 1
    assert menu[3] == 2
    assert menu[4] == 3
    assert json.loads(menu[5]) == {
        'recipe_id': TEST_RECIPE_1.recipe_id,
        'calories': TEST_RECIPE_1.nutrition.calories,
    }
    assert json.loads(menu[6]) == {
        'recipe_id': TEST_RECIPE_2.recipe_id,
        'calories': TEST_RECIPE_2.nutrition.calories,
    }
    assert json.loads(menu[7]) == {
        'recipe_id': TEST_RECIPE_3.recipe_id,
        'calories': TEST_RECIPE_3.nutrition.calories,
    }
