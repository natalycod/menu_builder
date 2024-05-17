#include <cstdarg>
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <map>
#include <unordered_set>
#include <optional>

const double CALORIES = 1000;
const double BREAKFAST_CALORIES = CALORIES * 1 / 3;
const double LUNCH_CALORIES = CALORIES * 2 / 5;
const double DINNER_CALORIES = CALORIES * 4 / 15;

const double CARBS_L = CALORIES * 10 / 100 / 4 + 1;
const double CARBS_R = CALORIES * 15 / 100 / 4 - 1;
const double FATS_L = CALORIES * 15 / 100 / 9 + 1;
const double FATS_R = CALORIES * 30 / 100 / 9 - 1;
const double PROTS_L = CALORIES * 55 / 100 / 4 + 1;
const double PROTS_R = CALORIES * 75 / 100 / 4 - 1;


struct Menu {
    std::vector<std::pair<std::string, std::string> > recipe_ids;
    double calories = -1;
    double carbohydrates = -1;
    double fats = -1;
    double proteins = -1;
    std::unordered_set<std::string> ingredients;

    int quality = 0;
};

struct Recipe {
    std::string type;
    std::string id;
    double calories;
    double carbohydrates;
    double fats;
    double proteins;
    std::unordered_set<std::string> ingredients;

    Recipe operator *(const double mult) const {
        Recipe result;
        result.type = this->type;
        result.id = this->id;
        result.calories = this->calories * mult;
        result.carbohydrates = this->carbohydrates * mult;
        result.fats = this->fats * mult;
        result.proteins = this->proteins * mult;
        result.ingredients = this->ingredients;
        return result;
    }

    Menu operator +(const Recipe& other) const {
        Menu result;
        result.recipe_ids.push_back(std::make_pair(this->type, this->id));
        result.recipe_ids.push_back(std::make_pair(other.type, other.id));

        result.calories = this->calories + other.calories;
        result.carbohydrates = this->carbohydrates + other.carbohydrates;
        result.fats = this->fats + other.fats;
        result.proteins = this->proteins + other.proteins;
        result.ingredients = std::unordered_set<std::string>();
        for (const auto& ingr : this->ingredients) {
            if (result.ingredients.count(ingr)) {
                result.quality++;
            }
            result.ingredients.insert(ingr);
        }
        for (const auto& ingr : other.ingredients) {
            if (result.ingredients.count(ingr)) {
                result.quality++;
            }
            result.ingredients.insert(ingr);
        }
        return result;
    }
};

Menu operator +(const Menu& menu, const Recipe& recipe) {
    Menu result;
    result.calories = menu.calories + recipe.calories;
    result.carbohydrates = menu.carbohydrates + recipe.carbohydrates;
    result.fats = menu.fats + recipe.fats;
    result.proteins = menu.proteins + recipe.proteins;

    result.recipe_ids = menu.recipe_ids;
    result.recipe_ids.push_back(std::make_pair(recipe.type, recipe.id));
    result.ingredients = menu.ingredients;
    for (const auto& ingr : recipe.ingredients) {
        if (result.ingredients.count(ingr)) {
            result.quality++;
        }
        result.ingredients.insert(ingr);
    }

    return result;
}

std::vector<std::string> split_by_delimeter(std::string s, char delimeter) {
    std::vector<std::string> result;
    std::string t = "";
    for (size_t i = 0; i < s.size(); ++i) {
        if (s[i] == delimeter) {
            result.push_back(t);
            t = "";
        } else {
            t += s[i];
        }
    }
    result.push_back(t);
    return result;
}

Recipe build_recipe_from_strings(const std::string& s, const std::string& t) {
    std::vector<std::string> values = split_by_delimeter(s, ' ');
    Recipe result;
    result.type = values[0];
    result.id = values[1];
    result.calories = stod(values[2]);
    result.carbohydrates = stod(values[3]);
    result.fats = stod(values[4]);
    result.proteins = stod(values[5]);

    std::vector<std::string> ingrs = split_by_delimeter(t, ' ');
    for (const std::string& ingr : ingrs) {
        result.ingredients.insert(ingr);
    }

    return result;
}

std::vector<Recipe> read_recipes_from_file(std::string filename) {
    std::vector<Recipe> result;

    std::ifstream file(filename);
    std::string s, t;
    while (getline(file, s) && getline(file, t)) {
        Recipe now = build_recipe_from_strings(s, t);
        result.push_back(now);
    }
    file.close();

    return result;
}

void normalize(std::vector<Recipe>& recipes, const double calories) {
    for (Recipe& recipe : recipes) {
        double mult = calories / recipe.calories;
        recipe.calories *= mult;
        recipe.carbohydrates *= mult;
        recipe.fats *= mult;
        recipe.proteins *= mult;
    }
}

std::vector<Recipe> get_random_sample(const std::vector<Recipe>& vect, const int amount) {
    std::vector<Recipe> result = vect;
    std::random_shuffle(result.begin(), result.end());
    while (result.size() > amount) {
        result.pop_back();
    }
    return result;
}

int math_round(const double x) {
    return int(x + 0.5);
}

bool is_balanced_menu(const Menu& menu) {
    if (menu.carbohydrates < CARBS_L || CARBS_R < menu.carbohydrates) {
        return false;
    }
    if (menu.fats < FATS_L || FATS_R < menu.fats) {
        return false;
    }
    return true;
}

std::vector<std::vector<Menu> > knapsack_step(std::vector<std::vector<Menu> >& dp, const std::vector<Recipe>& recipes) {
    std::vector<std::vector<Menu> > result;
    for (int carbs = 0; carbs <= CARBS_R; carbs++) {
        std::vector<Menu> resulti;
        for (int fats = 0; fats <= FATS_R; fats++) {
            Menu menu;
            resulti.push_back(menu);
        }
        result.push_back(resulti);
    }

    for (int carbs = 0; carbs <= CARBS_R; carbs++) {
        for (int fats = 0; fats <= FATS_R; fats++) {
            if (dp[carbs][fats].calories == -1) {
                continue;
            }
            for (const auto& recipe : recipes) {
                const Menu menu_new = dp[carbs][fats] + recipe;
                int carbs_new = math_round(menu_new.carbohydrates);
                int fats_new = math_round(menu_new.fats);
                
                if (carbs_new > CARBS_R || fats_new > FATS_R) {
                    continue;
                }
                else if (result[carbs_new][fats_new].calories == -1) {
                    result[carbs_new][fats_new] = menu_new;
                }
                else if (result[carbs_new][menu_new.fats].quality < menu_new.quality) {
                    result[carbs_new][fats_new] = menu_new;
                }
            }
        }
    }

    return result;
}

std::pair<int, int> knapsack_exp(std::vector<Recipe>& breakfasts, std::vector<Recipe>& lunches, std::vector<Recipe>& dinners) {
    int time_start = clock();
    std::vector<std::vector<Menu> > dp;
    for (int carbs = 0; carbs <= CARBS_R; carbs++) {
        std::vector<Menu> dpi;
        for (int fats = 0; fats <= FATS_R; fats++) {
            Menu menu;
            dpi.push_back(menu);
        }
        dp.push_back(dpi);
    }
    dp[0][0].calories = 0;
    dp[0][0].carbohydrates = 0;
    dp[0][0].fats = 0;
    dp[0][0].proteins = 0;

    dp = knapsack_step(dp, breakfasts);
    dp = knapsack_step(dp, lunches);
    dp = knapsack_step(dp, dinners);
    int max_quality = -1;
    for (int carbs = CARBS_L; carbs <= CARBS_R; carbs++) {
        for (int fats = FATS_L; fats <= FATS_R; fats++) {
            if (dp[carbs][fats].calories != -1 && dp[carbs][fats].quality > max_quality) {
                max_quality = dp[carbs][fats].quality;
            }
        }
    }
    int time_end = clock();
    return std::make_pair(max_quality, time_end - time_start);
}

int main() {
    std::vector<Recipe> breakfasts = read_recipes_from_file("data/breakfast.txt");
    normalize(breakfasts, BREAKFAST_CALORIES);
    std::vector<Recipe> lunches = read_recipes_from_file("data/lunch.txt");
    normalize(lunches, LUNCH_CALORIES);
    std::vector<Recipe> dinners = read_recipes_from_file("data/dinner.txt");
    normalize(dinners, DINNER_CALORIES);

    for (int amount = 10; amount <= 200; amount += 10) {
        std::vector<std::pair<int, int> > results;
        for (int i = 0; i < 100; i++) {
            std::vector<Recipe> bs = get_random_sample(breakfasts, amount);
            std::vector<Recipe> ls = get_random_sample(lunches, amount);
            std::vector<Recipe> ds = get_random_sample(dinners, amount);

            std::pair<int, int> result = knapsack_exp(bs, ls, ds);
            results.push_back(result);
        }

        int amount_success = 0;
        int sum_quality = 0;
        long long sum_ticks = 0;
        for (const auto& result : results) {
            if (result.first != -1) {
                amount_success++;
                sum_quality += result.first;
                sum_ticks += result.second;
            }
        }
        std::cout << "For amount = " << amount << ":\n";
        std::cout << "Successful: " << amount_success
                  << ", mean quality: " << (long double)(sum_quality) / amount_success
                  << ", mean ticks: " << (long double)(sum_ticks) / 100 << "\n";
    }
    return 0;
}
