import json

class Ingredient:
    def __init__(self, id : str = None, name : str = None, url : str = None, calories : float = None, carbs : float = None, fats : float = None, prots : float = None, unit : str = None, unit_amount : float = None):
        self.id = id
        self.name = name
        self.url = url

        self.calories = calories
        self.carbohydrates = carbs
        self.fats = fats
        self.proteins = prots

        self.unit = unit
        self.unit_amount = unit_amount
    
    def __mul__(self, x : float):
        return Ingredient(self.id, self.name, self.url, self.calories * x, self.carbohydrates * x, self.fats * x, self.proteins * x, self.unit, self.unit_amount * x)
    
    def __add__(self, other):
        return Ingredient(self.id, self.name, self.url, self.calories + other.calories, self.carbohydrates + other.carbohydrates, self.fats + other.fats, self.proteins + other.proteins, self.unit, self.unit_amount + other.unit_amount)


class Recipe:
    def __init__(self, recipe_id : str = None, calories : float = None, carbs : float = None, fats : float = None, proteins : float = None, recipe_url : str = None, recipe_name : str = None, ingredients : list = []):
        self.recipe_id = recipe_id
        self.calories = calories
        self.carbohydrates = carbs
        self.fats = fats
        self.proteins = proteins

        self.recipe_url = recipe_url
        self.recipe_name = recipe_name
        self.ingredients = ingredients

    def __mul__(self, x : float):
        ingredients_new = []
        for ingr in self.ingredients:
            ingredients_new.append(ingr * x)
        return Recipe(recipe_id=self.recipe_id, calories=self.calories * x, carbs=self.carbohydrates * x, fats=self.fats * x, proteins=self.proteins * x, recipe_url=self.recipe_url, recipe_name=self.recipe_name, ingredients=ingredients_new)

class Menu:
    def __init__(self):
        self.id = ""
        self.calories = 0
        self.carbohydrates = 0
        self.fats = 0
        self.proteins = 0
        self.recipes = []
    
    def __add__(self, recipe : Recipe):
        res = Menu()
        res.calories = self.calories + recipe.calories
        res.carbohydrates = self.carbohydrates + recipe.carbohydrates
        res.fats = self.fats + recipe.fats
        res.proteins = self.proteins + recipe.proteins
        res.recipes = self.recipes[:]
        res.recipes.append(recipe)
        return res


def serialize_recipe(recipe : Recipe) -> str:
    ingredients = []
    for ingr in recipe.ingredients:
        ingredients.append({
            "food_id": ingr.id,
            "food_name": ingr.name,
            "food_url": ingr.url,
            "calories": ingr.calories,
            "carbohydrates": ingr.carbohydrates,
            "fats": ingr.fats,
            "proteins": ingr.proteins,
            "unit": ingr.unit,
            "unit_amount": ingr.unit_amount,
        })

    return json.dumps({
        "recipe_id": recipe.recipe_id,
        "recipe_url": recipe.recipe_url,
        "recipe_name": recipe.recipe_name,
        "calories": recipe.calories,
        "carbohydrates": recipe.carbohydrates,
        "fats": recipe.fats,
        "proteins": recipe.proteins,
        "ingredients": ingredients
    })

def deserialize_recipe(s : str) -> Recipe:
    js = json.loads(s)
    ingredients = []
    for ingr in js['ingredients']:
        ingredients.append(Ingredient(ingr['food_id'], ingr['food_name'], ingr['food_url'], ingr['calories'], ingr['carbohydrates'], ingr['fats'], ingr['proteins'], ingr['unit'], ingr['unit_amount']))
    return Recipe(js['recipe_id'], js['calories'], js['carbohydrates'], js['fats'], js['proteins'], js['recipe_name'], js['recipe_url'])

def serialize_menu_to_json(menu : Menu):
    result = {
        "menu_id": menu.id,
        "nutrition": {
            "calories": menu.calories,
            "carbohydrates": menu.carbohydrates,
            "fats": menu.fats,
            "proteins": menu.proteins,
        },
        "breakfast_info": json.loads(serialize_recipe(menu.recipes[0])),
        "lunch_info": json.loads(serialize_recipe(menu.recipes[1])),
        "dinner_info": json.loads(serialize_recipe(menu.recipes[2])),
    }
    return result
