from utils.data_classes import Menu


def filter_knapsack(st, calories, carbs_seg, fats_seg, prots_seg):
    carbs_r = calories * carbs_seg[1] / 100 / 4
    fats_r = calories * fats_seg[1] / 100 / 9
    prots_r = calories * prots_seg[1] / 100 / 4
    
    new_s = set()
    for menu in st:
        if menu.nutrition.carbohydrates > carbs_r or menu.nutrition.fats > fats_r or menu.nutrition.proteins > prots_r:
            continue
        new_s.add(menu)
    return new_s

def final_filter_knapsack(st, calories, carbs_seg, fats_seg, prots_seg):
    carbs_l, carbs_r = calories * carbs_seg[0] / 100 / 4, calories * carbs_seg[1] / 100 / 4
    fats_l, fats_r = calories * fats_seg[0] / 100 / 9, calories * fats_seg[1] / 100 / 9
    prots_l, prots_r = calories * prots_seg[0] / 100 / 4, calories * prots_seg[1] / 100 / 4
    
    new_s = set()
    for menu in st:
        if menu.nutrition.carbohydrates > carbs_r or menu.nutrition.fats > fats_r or menu.nutrition.proteins > prots_r:
            continue
        if menu.nutrition.carbohydrates < carbs_l or menu.nutrition.fats < fats_l or menu.nutrition.proteins < prots_l:
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

def build_real_knapsack_step(dp, recipes, carbs_R, fats_R):
    result = []
    for carbs in range(int(carbs_R) + 1):
        resulti = []
        for fats in range(int(fats_R) + 1):
            resulti.append(None)
        result.append(resulti)

    for carbs in range(int(carbs_R) + 1):
        for fats in range(int(fats_R) + 1):
            if dp[carbs][fats] is None:
                continue
            for recipe in recipes:
                menu_new = dp[carbs][fats] + recipe
                carbs_new = int(menu_new.nutrition.carbohydrates)
                fats_new = int(menu_new.nutrition.fats)
                if carbs_new > int(carbs_R) or fats_new > int(fats_R):
                    continue
                if result[carbs_new][fats_new] is None:
                    result[carbs_new][fats_new] = menu_new
                if result[carbs_new][fats_new].quality < menu_new.quality:
                    result[carbs_new][fats_new] = menu_new

    return result


def build_real_knapsack(calories, recipe_stages, carbs_seg, fats_seg, prots_seg):
    dp = []
    carbs_L, carbs_R = 1000 * carbs_seg[0] / 100 / 4, 1000 * carbs_seg[1] / 100 / 4
    fats_L, fats_R = 1000 * fats_seg[0] / 100 / 9, 1000 * fats_seg[1] / 100 / 9

    for carbs in range(int(carbs_R) + 1):
        dpi = []
        for fats in range(int(fats_R) + 1):
            dpi.append(Menu())
        dp.append(dpi)

    for recipe_stage in recipe_stages:
        dp = build_real_knapsack_step(dp, recipe_stage, carbs_R, fats_R)
    
    result = []
    for carbs in range(int(carbs_L), int(carbs_R) + 1):
        for fats in range(int(fats_L), int(fats_R) + 1):
            if dp[carbs][fats] is None:
                continue
            result.append(dp[carbs][fats] * (calories / 1000))
    return result
