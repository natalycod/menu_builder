from data_classes import Menu


def filter_knapsack(st, calories, carbs_seg, fats_seg, prots_seg):
    carbs_l, carbs_r = calories * carbs_seg[0] / 100 / 4, calories * carbs_seg[1] / 100 / 4
    fats_l, fats_r = calories * fats_seg[0] / 100 / 4, calories * fats_seg[1] / 100 / 4
    prots_l, prots_r = calories * prots_seg[0] / 100 / 4, calories * prots_seg[1] / 100 / 4
    
    new_s = set()
    for menu in st:
        if menu.carbohydrates > carbs_r or menu.fats > fats_r or menu.proteins > prots_r:
            continue
        new_s.add(menu)
    return new_s

def final_filter_knapsack(st, calories, carbs_seg, fats_seg, prots_seg):
    carbs_l, carbs_r = calories * carbs_seg[0] / 100 / 4, calories * carbs_seg[1] / 100 / 4
    fats_l, fats_r = calories * fats_seg[0] / 100 / 4, calories * fats_seg[1] / 100 / 4
    prots_l, prots_r = calories * prots_seg[0] / 100 / 4, calories * prots_seg[1] / 100 / 4
    
    new_s = set()
    for menu in st:
        if menu.carbohydrates > carbs_r or menu.fats > fats_r or menu.proteins > prots_r:
            continue
        if menu.carbohydrates < carbs_l or menu.fats < fats_l or menu.proteins < prots_l:
            continue
        new_s.add(menu)
    return new_s

def build_knapsack_step(st, recipes):
    new_s = set()
    for menu in st:
        for recipe in recipes:
            new_menu = menu + recipe
            new_s.add(new_menu)
    return new_s

def build_knapsack(calories, recipe_stages, carbs_seg, fats_seg, prots_seg):
    s = set()
    s.add(Menu())

    for stage in recipe_stages:
        s = build_knapsack_step(s, stage)
        s = filter_knapsack(s, calories, carbs_seg, fats_seg, prots_seg)

    s = final_filter_knapsack(s, calories, carbs_seg, fats_seg, prots_seg)

    result = []
    for menu in s:
        result.append(menu)
    return result
