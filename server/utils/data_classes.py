import json

class Nutrition:
    def __init__(self, calories : float = None, carbs : float = None, fats : float = None, prots : float = None, js : dict = None):
        if js is None:
            self.calories = calories
            self.carbohydrates = carbs
            self.fats = fats
            self.proteins = prots
        else:
            self.calories = js['calories'] if 'calories' in js else None
            self.carbohydrates = js['carbohydrates'] if 'carbohydrates' in js else None
            self.fats = js['fats'] if 'fats' in js else None
            self.proteins = js['proteins'] if 'proteins' in js else None

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
            self.id = js['id'] if 'id' in js else None
            self.name = js['name'] if 'name' in js else None
            self.url = js['url'] if 'url' in js else None

            self.nutrition = Nutrition(js=js['nutrition']) if 'nutrition' in js else None

            self.unit = js['unit'] if 'unit' in js else None
            self.unit_amount = js['unit_amount'] if 'unit_amount' in js else None

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
    def __init__(self, recipe_id : str = None, nutrition : Nutrition = None, recipe_url : str = None, image_url : str = None, recipe_name : str = None, ingredients : list = [], instructions : list = [], js = None):
        if js is None:
            self.recipe_id = recipe_id
            self.recipe_name = recipe_name
            self.recipe_url = recipe_url
            self.image_url = image_url
            self.nutrition = nutrition
            self.ingredients = ingredients
            self.instructions = instructions
        else:
            self.recipe_id = js['recipe_id'] if 'recipe_id' in js else None
            self.recipe_name = js['name'] if 'name' in js else None
            self.recipe_url = js['url'] if 'url' in js else None
            self.image_url = js['image_url'] if 'image_url' in js else None
            self.nutrition = Nutrition(js=js['nutrition']) if 'nutrition' in js else None
            ingredients_res = []
            for ingr in ingredients:
                ingredients_res.append(Ingredient(js=ingr))
            self.ingredients = ingredients_res
            self.instructions = js['instructions'] if 'instructions' in js else None

    def __mul__(self, x : float):
        ingredients_new = []
        for ingr in self.ingredients:
            ingredients_new.append(ingr * x)
        return Recipe(recipe_id=self.recipe_id, nutrition=self.nutrition * x, recipe_url=self.recipe_url, image_url=self.image_url, recipe_name=self.recipe_name, ingredients=ingredients_new, instructions=self.instructions)

    def to_json(self):
        ingredients_json = []
        for ingr in self.ingredients:
            ingredients_json.append(ingr.to_json())
        return {
            'recipe_id': self.recipe_id,
            'name': self.recipe_name,
            'url': self.recipe_url,
            'image_url': self.image_url,
            'nutrition': self.nutrition.to_json(),
            'ingredients': ingredients_json,
            'instructions': self.instructions,
        }

class Menu:
    def __init__(self):
        self.id = ""
        self.nutrition = Nutrition(0, 0, 0, 0)
        self.recipes = []

        self.ingredients = set()
        self.quality = 0
    
    def __add__(self, recipe : Recipe):
        res = Menu()
        res.nutrition = self.nutrition + recipe.nutrition
        res.recipes = self.recipes[:]
        res.recipes.append(recipe)

        for ingr in recipe.ingredients:
            if ingr.id in res.ingredients:
                res.quality += 1
            res.ingredients.add(ingr.id)
        return res

    def __mul__(self, x : float):
        res = Menu()
        res.id = self.id
        res.nutrition = self.nutrition * x
        res.recipes = []
        for recipe in self.recipes:
            res.recipes.append(recipe * x)

        res.ingredients = self.ingredients
        res.quality = self.quality
        return res

    def to_json(self):
        return {
            "id": self.id,
            "nutrition": self.nutrition.to_json(),
            "breakfast_info": self.recipes[0].to_json(),
            "lunch_info": self.recipes[1].to_json(),
            "dinner_info": self.recipes[2].to_json(),
        }
    