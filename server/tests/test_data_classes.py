import pytest

import utils.data_classes as data_classes


@pytest.mark.parametrize(
    ('calories', 'carbs', 'fats', 'prots', 'js'),
    [
        pytest.param(100, 1, 2, 3, None),
        pytest.param(100, 1, 2, 3, {'calories': 100, 'carbohydrates': 1, 'fats': 2, 'proteins': 3}),
    ]
)
def test_nutrition_init(calories, carbs, fats, prots, js):
    if js is None:
        nutrition = data_classes.Nutrition(calories, carbs, fats, prots)
    else:
        nutrition = data_classes.Nutrition(js=js)

    assert nutrition.calories == calories
    assert nutrition.carbohydrates == carbs
    assert nutrition.fats == fats
    assert nutrition.proteins == prots


@pytest.mark.parametrize(
    ('cal', 'carb', 'fat', 'prot', 'mult_x', 'cal_res', 'carb_res', 'fat_res', 'prot_res'),
    [
        pytest.param(100, 1, 2, 3, 0, 0, 0, 0, 0),
        pytest.param(100, 1, 2, 3, 1, 100, 1, 2, 3),
        pytest.param(100, 1, 2, 3, 2.5, 250, 2.5, 5, 7.5),
    ]
)
def test_nutrition_mult(cal, carb, fat, prot, mult_x, cal_res, carb_res, fat_res, prot_res):
    nutrition = data_classes.Nutrition(cal, carb, fat, prot)
    nutrition_res = nutrition * mult_x
    
    assert nutrition_res.calories == cal_res
    assert nutrition_res.carbohydrates == carb_res
    assert nutrition_res.fats == fat_res
    assert nutrition_res.proteins == prot_res


@pytest.mark.parametrize(
    ('cal1', 'carb1', 'fat1', 'prot1', 'cal2', 'carb2', 'fat2', 'prot2', 'cal_res', 'carb_res', 'fat_res', 'prot_res'),
    [
        pytest.param(100, 1, 2, 3, 100, 1, 2, 3, 200, 2, 4, 6),
        pytest.param(100, 1, 2, 3, 0, 0, 0, 0, 100, 1, 2, 3),
        pytest.param(0, 0, 0, 0, 100, 1, 2, 3, 100, 1, 2, 3),
        pytest.param(1, 2, 3, 4, 5, 6, 7, 8, 6, 8, 10, 12),
        pytest.param(5, 6, 7, 8, 1, 2, 3, 4, 6, 8, 10, 12),
    ]
)
def test_nutrition_sum(cal1, carb1, fat1, prot1, cal2, carb2, fat2, prot2, cal_res, carb_res, fat_res, prot_res):
    nutrition1 = data_classes.Nutrition(cal1, carb1, fat1, prot1)
    nutrition2 = data_classes.Nutrition(cal2, carb2, fat2, prot2)
    nutrition_res = nutrition1 + nutrition2
    
    assert nutrition_res.calories == cal_res
    assert nutrition_res.carbohydrates == carb_res
    assert nutrition_res.fats == fat_res
    assert nutrition_res.proteins == prot_res


@pytest.mark.parametrize(
    ('calories', 'carbs', 'fats', 'prots', 'js_expected'),
    [
        pytest.param(100, 1, 2, 3, {'calories': 100, 'carbohydrates': 1, 'fats': 2, 'proteins': 3}),
        pytest.param(0, 0, 0, 0, {'calories': 0, 'carbohydrates': 0, 'fats': 0, 'proteins': 0}),
    ]
)
def test_nutrition_to_json(calories, carbs, fats, prots, js_expected):
    nutrition = data_classes.Nutrition(calories, carbs, fats, prots)
    nutrition_js = nutrition.to_json()

    assert nutrition_js == js_expected


@pytest.mark.parametrize(
    ('id', 'name', 'url', 'nutrition', 'unit', 'unit_amount', 'js'),
    [
        pytest.param('t_id', 't_name', 't_url', data_classes.Nutrition(1, 2, 3, 4), 't_unit', 100, None),
        pytest.param('t_id', 't_name', 't_url', data_classes.Nutrition(1, 2, 3, 4), 't_unit', 100,
                     {'id': 't_id', 'name': 't_name', 'url': 't_url', 'nutrition': {'calories': 1, 'carbohydrates': 2, 'fats': 3, 'proteins': 4}, 'unit': 't_unit', 'unit_amount': 100}),
    ]
)
def test_ingredient_init(id, name, url, nutrition, unit, unit_amount, js):
    if js is None:
        ingredient = data_classes.Ingredient(id, name, url, nutrition, unit, unit_amount)
    else:
        ingredient = data_classes.Ingredient(js=js)

    assert ingredient.id == id
    assert ingredient.name == name
    assert ingredient.url == url
    assert ingredient.unit == unit
    assert ingredient.unit_amount == unit_amount
    
    assert ingredient.nutrition.calories == nutrition.calories
    assert ingredient.nutrition.carbohydrates == nutrition.carbohydrates
    assert ingredient.nutrition.fats == nutrition.fats
    assert ingredient.nutrition.proteins == nutrition.proteins


@pytest.mark.parametrize(
    ('nutrition', 'unit_amount', 'mult_x', 'nutrition_res', 'unit_amount_res'),
    [
        pytest.param(data_classes.Nutrition(100, 1, 2, 3), 42, 0, data_classes.Nutrition(0, 0, 0, 0), 0),
        pytest.param(data_classes.Nutrition(100, 1, 2, 3), 42, 1, data_classes.Nutrition(100, 1, 2, 3), 42),
        pytest.param(data_classes.Nutrition(100, 1, 2, 3), 42, 2.5, data_classes.Nutrition(250, 2.5, 5, 7.5), 105),
    ]
)
def test_ingredient_mult(nutrition, unit_amount, mult_x, nutrition_res, unit_amount_res):
    ingredient = data_classes.Ingredient("t_id", "t_name", "t_url", nutrition, "t_unit", unit_amount)
    ingredient_res = ingredient * mult_x

    assert ingredient_res.id == "t_id"
    assert ingredient_res.name == "t_name"
    assert ingredient_res.url == "t_url"
    assert ingredient_res.unit == "t_unit"
    assert ingredient_res.unit_amount == unit_amount_res
    
    assert ingredient_res.nutrition.calories == nutrition_res.calories
    assert ingredient_res.nutrition.carbohydrates == nutrition_res.carbohydrates
    assert ingredient_res.nutrition.fats == nutrition_res.fats
    assert ingredient_res.nutrition.proteins == nutrition_res.proteins


@pytest.mark.parametrize(
    ('nutrition1', 'unit_amount1', 'nutrition2', 'unit_amount2', 'nutrition_res', 'unit_amount_res'),
    [
        pytest.param(data_classes.Nutrition(100, 1, 2, 3), 42, data_classes.Nutrition(100, 1, 2, 3), 42, data_classes.Nutrition(200, 2, 4, 6), 84),
        pytest.param(data_classes.Nutrition(100, 1, 2, 3), 42, data_classes.Nutrition(0, 0, 0, 0), 0, data_classes.Nutrition(100, 1, 2, 3), 42),
        pytest.param(data_classes.Nutrition(0, 0, 0, 0), 0, data_classes.Nutrition(100, 1, 2, 3), 42, data_classes.Nutrition(100, 1, 2, 3), 42),
        pytest.param(data_classes.Nutrition(1, 2, 3, 4), 42, data_classes.Nutrition(5, 6, 7, 8), 31, data_classes.Nutrition(6, 8, 10, 12), 73),
        pytest.param(data_classes.Nutrition(5, 6, 7, 8), 31, data_classes.Nutrition(1, 2, 3, 4), 42, data_classes.Nutrition(6, 8, 10, 12), 73),
    ]
)
def test_ingredient_sum(nutrition1, unit_amount1, nutrition2, unit_amount2, nutrition_res, unit_amount_res):
    ingredient1 = data_classes.Ingredient("t_id", "t_name", "t_url", nutrition1, "t_unit", unit_amount1)
    ingredient2 = data_classes.Ingredient("t_id", "t_name", "t_url", nutrition2, "t_unit", unit_amount2)
    ingredient_res = ingredient1 + ingredient2

    assert ingredient_res.id == "t_id"
    assert ingredient_res.name == "t_name"
    assert ingredient_res.url == "t_url"
    assert ingredient_res.unit == "t_unit"
    assert ingredient_res.unit_amount == unit_amount_res
    
    assert ingredient_res.nutrition.calories == nutrition_res.calories
    assert ingredient_res.nutrition.carbohydrates == nutrition_res.carbohydrates
    assert ingredient_res.nutrition.fats == nutrition_res.fats
    assert ingredient_res.nutrition.proteins == nutrition_res.proteins


@pytest.mark.parametrize(
    ('nutrition', 'unit_amount', 'js_expected'),
    [
        pytest.param(data_classes.Nutrition(100, 1, 2, 3), 42,
                     {
                         'id': 't_id',
                         'name': 't_name',
                         'url': 't_url',
                         'nutrition': {'calories': 100, 'carbohydrates': 1, 'fats': 2, 'proteins': 3},
                         'unit': 't_unit',
                         'unit_amount': 42,
                     }),
        pytest.param(data_classes.Nutrition(0, 0, 0, 0), 0,
                     {
                         'id': 't_id',
                         'name': 't_name',
                         'url': 't_url',
                         'nutrition': {'calories': 0, 'carbohydrates': 0, 'fats': 0, 'proteins': 0},
                         'unit': 't_unit',
                         'unit_amount': 0,
                     }),
    ]
)
def test_ingredient_to_json(nutrition, js_expected, unit_amount):
    ingredient = data_classes.Ingredient("t_id", "t_name", "t_url", nutrition, "t_unit", unit_amount)
    ingredient_js = ingredient.to_json()

    assert ingredient_js == js_expected
