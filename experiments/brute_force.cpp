#include <cstdarg>
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <map>
#include <unordered_set>

const double CALORIES = 1000;
const double BREAKFAST_CALORIES = CALORIES * 1 / 3;
const double LUNCH_CALORIES = CALORIES * 2 / 5;
const double DINNER_CALORIES = CALORIES * 4 / 15;

const double CARBS_L = CALORIES * 10 / 100 / 4;
const double CARBS_R = CALORIES * 15 / 100 / 4;
const double FATS_L = CALORIES * 15 / 100 / 9;
const double FATS_R = CALORIES * 30 / 100 / 9;
const double PROTS_L = CALORIES * 55 / 100 / 4;
const double PROTS_R = CALORIES * 75 / 100 / 4;


struct Menu {
    std::vector<std::pair<std::string, std::string> > recipe_ids;
    double calories = 0;
    double carbohydrates = 0;
    double fats = 0;
    double proteins = 0;
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

bool is_balanced_menu(const Menu& menu) {
    if (menu.carbohydrates < CARBS_L || CARBS_R < menu.carbohydrates) {
        return false;
    }
    if (menu.fats < FATS_L || FATS_R < menu.fats) {
        return false;
    }
    if (menu.proteins < PROTS_L || PROTS_R < menu.proteins) {
        return false;
    }
    return true;
}

std::pair<int, int> brute_force_exp(std::vector<Recipe> breakfasts, std::vector<Recipe> lunches, std::vector<Recipe> dinners) {
    int cnt_balanced = 0;
    int max_quality = -1;
    int time_start = clock();
    for (const Recipe& breakfast : breakfasts) {
        for (const Recipe& lunch : lunches) {
            for (const Recipe& dinner : dinners) {
                Menu menu = breakfast + lunch + dinner;
                if (is_balanced_menu(menu)) {
                    if (menu.quality > max_quality) {
                        max_quality = menu.quality;
                    }
                    cnt_balanced += 1;
                }
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

    std::cout << "For future calculating: CLOCKS_PER_SEC = " << (double)CLOCKS_PER_SEC << "\n";

    for (int amount = 10; amount <= 100; amount += 10) {
        std::vector<std::pair<int, int> > results;
        for (int i = 0; i < 100; i++) {
            std::vector<Recipe> bs = get_random_sample(breakfasts, amount);
            std::vector<Recipe> ls = get_random_sample(lunches, amount);
            std::vector<Recipe> ds = get_random_sample(dinners, amount);

            std::pair<int, int> result = brute_force_exp(bs, ls, ds);
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
