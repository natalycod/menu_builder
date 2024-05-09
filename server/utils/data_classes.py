import json

class Nutrition:
    def __init__(self, calories : float = None, carbs : float = None, fats : float = None, prots : float = None, js : dict = None):
        if js is None:
            self.calories = calories
            self.carbohydrates = carbs
            self.fats = fats
            self.proteins = prots
        else:
            self.calories = js['calories']
            self.carbohydrates = js['carbohydrates']
            self.fats = js['fats']
            self.proteins = js['proteins']

    def __mul__(self, x : float):
        return Nutrition(self.calories * x, self.carbohydrates * x, self.fats * x, self.proteins * x)

    def __add__(self, other):
        return Nutrition(self.calories + other.calories, self.carbohydrates + other.carbohydrates, self.fats + other.fats, self.proteins + other.proteins)

    def to_json(self):
        return {
            'calories': self.calories,
            'carbohydrates': self.carbohydrates,
            'fats': self.fats,
            'proteins': self.proteins,
        }

class Ingredient:
    def __init__(self, id : str = None, name : str = None, url : str = None, nutrition : Nutrition = None, unit : str = None, unit_amount : float = None, js : dict = None):
        if js is None:
            self.id = id
            self.name = name
            self.url = url

            self.nutrition = nutrition

            self.unit = unit
            self.unit_amount = unit_amount
        else:
            self.id = js['id']
            self.name = js['name']
            self.url = js['url']

            self.nutrition = Nutrition(js=js['nutrition'])

            self.unit = js['unit']
            self.unit_amount = js['unit_amount']

    def __mul__(self, x : float):
        return Ingredient(self.id, self.name, self.url, self.nutrition * x if self.nutrition is not None else None, self.unit, self.unit_amount * x)

    def __add__(self, other):
        return Ingredient(self.id, self.name, self.url, self.nutrition + other.nutrition, self.unit, self.unit_amount + other.unit_amount)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "nutrition": self.nutrition.to_json() if self.nutrition is not None else None,
            "unit": self.unit,
            "unit_amount": self.unit_amount,
        }


class Recipe:
    def __init__(self, recipe_id : str = None, nutrition : Nutrition = None, recipe_url : str = None, recipe_name : str = None, ingredients : list = [], js = None):
        if js is None:
            self.recipe_id = recipe_id
            self.recipe_name = recipe_name
            self.recipe_url = recipe_url
            self.nutrition = nutrition
            self.ingredients = ingredients
        else:
            self.recipe_id = js['recipe_id']
            self.recipe_name = js['name']
            self.recipe_url = js['url']
            self.nutrition = Nutrition(js=js['nutrition'])
            ingredients_res = []
            for ingr in ingredients:
                ingredients_res.append(Ingredient(js=ingr))
            self.ingredients = ingredients_res

    def __mul__(self, x : float):
        ingredients_new = []
        for ingr in self.ingredients:
            ingredients_new.append(ingr * x)
        return Recipe(recipe_id=self.recipe_id, nutrition=self.nutrition * x, recipe_url=self.recipe_url, recipe_name=self.recipe_name, ingredients=ingredients_new)

    def to_json(self):
        ingredients_json = []
        for ingr in self.ingredients:
            ingredients_json.append(ingr.to_json())
        return {
            'recipe_id': self.recipe_id,
            'name': self.recipe_name,
            'url': self.recipe_url,
            'nutrition': self.nutrition.to_json(),
            'ingredients': ingredients_json,
        }

class Menu:
    def __init__(self):
        self.id = ""
        self.nutrition = Nutrition(0, 0, 0, 0)
        self.recipes = []
    
    def __add__(self, recipe : Recipe):
        res = Menu()
        res.nutrition = self.nutrition + recipe.nutrition
        res.recipes = self.recipes[:]
        res.recipes.append(recipe)
        return res
    
    def to_json(self):
        return {
            "id": self.id,
            "nutrition": self.nutrition.to_json(),
            "breakfast_info": self.recipes[0].to_json(),
            "lunch_info": self.recipes[1].to_json(),
            "dinner_info": self.recipes[2].to_json(),
        }
