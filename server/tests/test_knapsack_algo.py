import pytest

import utils.knapsack_algo as knapsack_algo
from utils.data_classes import Menu, Recipe, Nutrition


@pytest.mark.parametrize(
    ('nutrition', 'calories', 'carbs_seg', 'fats_seg', 'prots_seg', 'is_correct'),
    [
        pytest.param(Nutrition(1000, 100, 100, 100), 1000, [0, 100], [0, 100], [0, 100], True, id="any is ok"),
        pytest.param(Nutrition(1000, 100, 100, 100), 1000, [0, 0], [0, 100], [0, 100], False, id="need 0 carb"),
        pytest.param(Nutrition(1000, 100, 100, 100), 1000, [0, 100], [0, 0], [0, 100], False, id="need 0 fat"),
        pytest.param(Nutrition(1000, 100, 100, 100), 1000, [0, 100], [0, 100], [0, 0], False, id="need 0 prot"),
        pytest.param(Nutrition(700, 37.5, 33.3, 187.5), 1000, [10, 15], [15, 30], [55, 75], True, id="menu is ok"),
        pytest.param(Nutrition(700, 38, 33.3, 187.5), 1000, [10, 15], [15, 30], [55, 75], False, id="too much carb"),
        pytest.param(Nutrition(700, 37.5, 33.5, 187.5), 1000, [10, 15], [15, 30], [55, 75], False, id="too much fat"),
        pytest.param(Nutrition(700, 37.5, 33.3, 187.6), 1000, [10, 15], [15, 30], [55, 75], False, id="too much prot"),
        pytest.param(Nutrition(100, 0, 0, 0), 1000, [10, 15], [15, 30], [55, 75], True, id="everything is low"),
    ]
)
def test_filter_knapsack(nutrition, calories, carbs_seg, fats_seg, prots_seg, is_correct):
    menu = Menu()
    menu.nutrition = nutrition
    s = set()
    s.add(menu)
    result = knapsack_algo.filter_knapsack(s, calories, carbs_seg, fats_seg, prots_seg)
    assert len(result) == (1 if is_correct else 0)


@pytest.mark.parametrize(
    ('nutrition', 'calories', 'carbs_seg', 'fats_seg', 'prots_seg', 'is_correct'),
    [
        pytest.param(Nutrition(1000, 100, 100, 100), 1000, [0, 100], [0, 100], [0, 100], True, id="any is ok"),
        pytest.param(Nutrition(1000, 100, 100, 100), 1000, [0, 0], [0, 100], [0, 100], False, id="need 0 carb"),
        pytest.param(Nutrition(1000, 100, 100, 100), 1000, [0, 100], [0, 0], [0, 100], False, id="need 0 fat"),
        pytest.param(Nutrition(1000, 100, 100, 100), 1000, [0, 100], [0, 100], [0, 0], False, id="need 0 prot"),
        pytest.param(Nutrition(700, 37.5, 33.3, 187.5), 1000, [10, 15], [15, 30], [55, 75], True, id="menu is ok high"),
        pytest.param(Nutrition(700, 38, 33.3, 187.5), 1000, [10, 15], [15, 30], [55, 75], False, id="too much carb"),
        pytest.param(Nutrition(700, 37.5, 33.5, 187.5), 1000, [10, 15], [15, 30], [55, 75], False, id="too much fat"),
        pytest.param(Nutrition(700, 37.5, 33.3, 187.6), 1000, [10, 15], [15, 30], [55, 75], False, id="too much prot"),
        pytest.param(Nutrition(700, 25, 16.7, 137.5), 1000, [10, 15], [15, 30], [55, 75], True, id="menu is ok low"),
        pytest.param(Nutrition(700, 24.99, 16.7, 137.5), 1000, [10, 15], [15, 30], [55, 75], False, id="too low carb"),
        pytest.param(Nutrition(700, 25, 16, 137.5), 1000, [10, 15], [15, 30], [55, 75], False, id="too low fat"),
        pytest.param(Nutrition(700, 25, 16.7, 137.4), 1000, [10, 15], [15, 30], [55, 75], False, id="too low prot"),
        pytest.param(Nutrition(100, 0, 0, 0), 1000, [10, 15], [15, 30], [55, 75], False, id="everything is low"),
    ]
)
def test_final_filter_knapsack(nutrition, calories, carbs_seg, fats_seg, prots_seg, is_correct):
    menu = Menu()
    menu.nutrition = nutrition
    s = set()
    s.add(menu)
    result = knapsack_algo.final_filter_knapsack(s, calories, carbs_seg, fats_seg, prots_seg)
    assert len(result) == (1 if is_correct else 0)


@pytest.mark.parametrize(
    ('menues_nutritions', 'recipes_nutritions'),
    [
        pytest.param([], [Nutrition(10, 1, 1, 1)]),
        pytest.param([Nutrition(1000, 10, 10, 10)], []),
        pytest.param([Nutrition(1000, 10, 10, 10)], [Nutrition(10, 1, 1, 1)]),
        pytest.param([Nutrition(1000, 10, 10, 10)], [Nutrition(10, 1, 1, 1), Nutrition(20, 1, 1, 1)]),
        pytest.param([Nutrition(1000, 10, 10, 10), Nutrition(2000, 10, 20, 30)], [Nutrition(10, 1, 2, 3), Nutrition(20, 2, 3, 4)]),
    ]
)
def test_build_knapsack_step(menues_nutritions, recipes_nutritions):
    s = set()
    for menu_nutrition in menues_nutritions:
        menu = Menu()
        menu.nutrition = menu_nutrition
        s.add(menu)

    assert len(s) == len(menues_nutritions)
    
    recipes = []
    for recipe_nutrition in recipes_nutritions:
        recipe = Recipe(nutrition=recipe_nutrition)
        recipes.append(recipe)
    
    assert len(recipes) == len(recipes_nutritions)

    result = knapsack_algo.build_knapsack_step(s, recipes)
    assert len(result) == len(s) * len(recipes)

    nutritions_built = []
    for menu_result in result:
        nutritions_built.append(menu_result.nutrition)

    for menu_nutrition in menues_nutritions:
        for recipe_nutrition in recipes_nutritions:
            nutrition_sum = menu_nutrition + recipe_nutrition
            is_in_nutritions_built = False
            for nutr in nutritions_built:
                if nutr.calories == nutrition_sum.calories and nutr.carbohydrates == nutrition_sum.carbohydrates and nutr.fats == nutrition_sum.fats and nutr.proteins == nutrition_sum.proteins:
                    is_in_nutritions_built = True
            assert is_in_nutritions_built


@pytest.mark.parametrize(
    ('calories', 'stages_nutritions', 'carbs_seg', 'fats_seg', 'prots_seg', 'menues_cnt_expected'),
    [
        pytest.param(1000, [[Nutrition(1000, 10, 20, 30)]], [0, 100], [0, 100], [0, 100], 1, id="1 stage - ok"),
        pytest.param(1000, [[Nutrition(1000, 10, 20, 30)]], [100, 100], [0, 100], [0, 100], 0, id="1 stage - too low carbs"),
        pytest.param(1000, [[Nutrition(1000, 10, 20, 30)]], [0, 100], [100, 100], [0, 100], 0, id="1 stage - too low fats"),
        pytest.param(1000, [[Nutrition(1000, 10, 20, 30)]], [0, 100], [0, 100], [100, 100], 0, id="1 stage - too low proteins"),
        pytest.param(1000, [[Nutrition(1000, 10, 20, 30)]], [0, 0], [0, 100], [0, 100], 0, id="1 stage - too much carbs"),
        pytest.param(1000, [[Nutrition(1000, 10, 20, 30)]], [0, 100], [0, 0], [0, 100], 0, id="1 stage - too much fats"),
        pytest.param(1000, [[Nutrition(1000, 10, 20, 30)]], [0, 100], [0, 100], [0, 0], 0, id="1 stage - too much proteins"),
        pytest.param(1000, [[Nutrition(500, 20, 10, 70), Nutrition(500, 20, 10, 70)], [Nutrition(500, 10, 10, 100), Nutrition(500, 10, 10, 100)]], [10, 15], [15, 30], [55, 75], 4, id="2 stages - ok"),
        pytest.param(1000, [[Nutrition(500, 0, 0, 0), Nutrition(500, 37.5, 33.3, 187.5)], [Nutrition(500, 0, 0, 0), Nutrition(500, 37.5, 33.3, 187.5)]], [10, 15], [15, 30], [55, 75], 2, id="2 stages - filtered"),
    ]
)
def test_build_knapsack(calories, stages_nutritions, carbs_seg, fats_seg, prots_seg, menues_cnt_expected):
    recipe_stages = []
    for stage in stages_nutritions:
        recipe_stage = []
        for nutrition in stage:
            recipe = Recipe(nutrition=nutrition)
            recipe_stage.append(recipe)
        recipe_stages.append(recipe_stage)

    result = knapsack_algo.build_knapsack(calories, recipe_stages, carbs_seg, fats_seg, prots_seg)

    assert len(result) == menues_cnt_expected
