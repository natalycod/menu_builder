import json
import random
import db_utils

from data_classes import Recipe, Menu, serialize_menu_to_json
import utils.knapsack_algo as knapsack_algo

MAX_CALORIES_DIFF = 0.2
CARBS_L, CARBS_R = 10, 15
FATS_L, FATS_R = 15, 30
PROTS_L, PROTS_R = 55, 75

RECIPES_AMOUNT_PER_MEAL = 60
RECIPES_VAR_AMOUNT = 1
BREAKFAST_PART = 1 / 3
LUNCH_PART = 2 / 5
DINNER_PART = 4 / 15

def build_calories_goals(ideal_cal : float, cnt : int) -> list:
    arr = []
    if cnt == 0:
        return arr
    if cnt == 1:
        arr.append(ideal_cal)
        return arr
    min_cal = ideal_cal * (1 - MAX_CALORIES_DIFF)
    max_cal = ideal_cal * (1 + MAX_CALORIES_DIFF)
    delta = (max_cal - min_cal) / (cnt - 1)
    for i in range(cnt):
        arr.append(min_cal + i * delta)
    return arr

def prepare_recipes(recipes : list, ideal_calories : float, cnt : int):
    cal_goals = build_calories_goals(ideal_calories, cnt)
    result = []
    for recipe in recipes:
        for cal in cal_goals:
            mult = cal / recipe.calories
            result.append(recipe * mult)

    return result

def get_recipes_variations(type : str, fixed_id : str):
    if fixed_id is None:
        return db_utils.get_random_recipes(type, RECIPES_AMOUNT_PER_MEAL)
    return [db_utils.get_recipe_by_id(fixed_id)]

def main(body):
    calories = 0
    for calorie in body['calories']:
        calories += float(calorie)

    menues = []
    while len(menues) == 0:
        breakfasts = get_recipes_variations("breakfast", body['breakfast_id'] if 'breakfast_id' in body else None)
        lunches = get_recipes_variations("lunch", body['lunch_id'] if 'lunch_id' in body else None)
        dinners = get_recipes_variations("dinner", body['dinner_id'] if 'dinner_id' in body else None)

        bs = prepare_recipes(breakfasts, calories * BREAKFAST_PART, RECIPES_VAR_AMOUNT)
        ls = prepare_recipes(lunches, calories * LUNCH_PART, RECIPES_VAR_AMOUNT)
        ds = prepare_recipes(dinners, calories * DINNER_PART, RECIPES_VAR_AMOUNT)

        menues = knapsack_algo.build_knapsack(calories, [bs, ls, ds], [CARBS_L, CARBS_R], [FATS_L, FATS_R], [PROTS_L, PROTS_R])

    menu = menues[random.randint(0, len(menues) - 1)]

    menu.id = db_utils.generate_id()
    db_utils.save_menu(menu)

    return serialize_menu_to_json(menu)
