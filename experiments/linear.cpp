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
const double E = 0.2;

const double CARBS_L = CALORIES * 10 / 100 / 4;
const double CARBS_R = CALORIES * 15 / 100 / 4;
const double FATS_L = CALORIES * 15 / 100 / 9;
const double FATS_R = CALORIES * 30 / 100 / 9;
const double PROTS_L = CALORIES * 55 / 100 / 4;
const double PROTS_R = CALORIES * 75 / 100 / 4;

const double IDEAL_CARBS = CALORIES * 15 / 100 / 4;
const double IDEAL_FATS = CALORIES * 30 / 100 / 9;
const double IDEAL_PROTS = CALORIES * 55 / 100 / 4;

struct Matrix {
    std::vector<std::vector<double> > matr;

    Matrix(std::vector<std::vector<double> > vect) {
        matr = vect;
    }

    Matrix operator *(const Matrix& other) const& {
        std::vector<std::vector<double> > vect;
        for (int i = 0; i < matr.size(); i++) {
            std::vector<double> vect2;
            for (int j = 0; j < other.matr[0].size(); j++) {
                vect2.push_back(0);
                for (int k = 0; k < other.matr.size(); k++) {
                    vect2[j] += matr[i][k] * other.matr[k][j];
                }
            }
            vect.push_back(vect2);
        }
        return Matrix(vect);
    }

    Matrix FindInv() {
        std::vector<std::vector<double> > inv = matr;
        std::vector<std::vector<double> > result;
        for (int i = 0; i < matr.size(); i++) {
            std::vector<double> result2;
            for (int j = 0; j < matr.size(); j++) {
                result2.push_back(i == j ? 1 : 0);
            }
            result.push_back(result2);
        }

        for (int i = 0; i < inv.size(); i++) {
            int j_ = i;
            while (j_ < inv.size() && inv[i][j_] == 0) {
                j_++;
            }
            if (j_ == inv.size()) {
                result = std::vector<std::vector<double> >();
                break;
            }
            std::swap(inv[i], inv[j_]);
            std::swap(result[i], result[j_]);

            for (int j = i + 1; j < inv.size(); j++) {
                double mult = inv[j][i] / inv[i][i];
                for (int k = 0; k < inv[j].size(); k++) {
                    inv[j][k] -= inv[i][k] * mult;
                    result[j][k] -= result[i][k] * mult;
                }
            }
        }

        for (int i = inv.size() - 1; i >= 0; i--) {
            for (int j = i - 1; j >= 0; j--) {
                double mult = inv[j][i] / inv[i][i];
                inv[j][i] -= inv[i][i] * mult;
                for (int k = 0; k < result.size(); k++) {
                    result[j][k] -= result[i][k] * mult;
                }
            }
        }

        for (int i = 0; i < inv.size(); i++) {
            double del = inv[i][i];
            inv[i][i] /= del;
            for (int k = 0; k < result.size(); k++) {
                result[i][k] /= del;
            }
        }
        return Matrix(result);
    }
};


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

std::vector<double> find_solution(const Recipe& breakfast, const Recipe& lunch, const Recipe& dinner, const double carb, const double fat, const double prot) {
    std::vector<double> carbs, fats, prots;
    carbs.push_back(breakfast.carbohydrates);
    carbs.push_back(lunch.carbohydrates);
    carbs.push_back(dinner.carbohydrates);
    
    fats.push_back(breakfast.fats);
    fats.push_back(lunch.fats);
    fats.push_back(dinner.fats);

    prots.push_back(breakfast.proteins);
    prots.push_back(lunch.proteins);
    prots.push_back(dinner.proteins);

    std::vector<std::vector<double> > nutrs;
    nutrs.push_back(carbs);
    nutrs.push_back(fats);
    nutrs.push_back(prots);

    Matrix x(nutrs);
    
    std::vector<std::vector<double> > need;
    need.push_back(std::vector<double>());
    need.push_back(std::vector<double>());
    need.push_back(std::vector<double>());
    need[0].push_back(carb);
    need[1].push_back(fat);
    need[2].push_back(prot);

    Matrix inv = x.FindInv();
    if (inv.matr.size() == 0) {
        return std::vector<double>();
    }
    Matrix res = inv * need;

    std::vector<double> result;
    result.push_back(res.matr[0][0]);
    result.push_back(res.matr[1][0]);
    result.push_back(res.matr[2][0]);
    return result;
}

bool is_good_solution(const Recipe& breakfast, const Recipe& lunch, const Recipe& dinner) {
    if (breakfast.calories < BREAKFAST_CALORIES * (1 - E) || BREAKFAST_CALORIES * (1 + E) < breakfast.calories) {
        return false;
    }
    if (lunch.calories < LUNCH_CALORIES * (1 - E) || LUNCH_CALORIES * (1 + E) < lunch.calories) {
        return false;
    }
    if (dinner.calories < DINNER_CALORIES * (1 - E) || DINNER_CALORIES * (1 + E) < dinner.calories) {
        return false;
    }
    return true;
}

std::pair<int, int> linear_exp(const std::vector<Recipe>& breakfasts, const std::vector<Recipe>& lunches, const std::vector<Recipe>& dinners, const int amount) {
    int max_quality = -1;
    int time_start = clock();
    for (int i = 0; i < amount; i++) {
        int id1 = rand() % breakfasts.size();
        int id2 = rand() % lunches.size();
        int id3 = rand() % dinners.size();
        std::vector<double> result = find_solution(breakfasts[id1], lunches[id2], dinners[id3], IDEAL_CARBS, IDEAL_FATS, IDEAL_PROTS);
        if (result.size() == 3 && is_good_solution(breakfasts[id1] * result[0], lunches[id2] * result[1], dinners[id3] * result[2])) {
            Menu menu = breakfasts[id1] + lunches[id2] + dinners[id3];
            if (menu.quality > max_quality) {
                max_quality = menu.quality;
            }
        }
    }
    int time_end = clock();
    return std::make_pair(max_quality, time_end - time_start);
}

double gen_random_double(double L, double R, int precision = 2) {
    int step = 1;
    for (int i = 0; i < precision; i++) {
        step *= 10;
    }
    int L_real = L * step;
    int R_real = R * step;

    int result = L_real + rand() % (R_real - L_real);
    return (double)result / step;
}

std::pair<int, int> linear_exp_random_balance(const std::vector<Recipe>& breakfasts, const std::vector<Recipe>& lunches, const std::vector<Recipe>& dinners, const int amount_gen, const int amount_choices) {
    int max_quality = -1;
    int time_start = clock();
    for (int i = 0; i < amount_gen; i++) {
        int id1 = rand() % breakfasts.size();
        int id2 = rand() % lunches.size();
        int id3 = rand() % dinners.size();

        for (int j = 0; j < amount_choices; j++) {
            double carbs_now = gen_random_double(CARBS_L, CARBS_R);
            double fats_now = gen_random_double(FATS_L, FATS_R);
            double prots_now = (CALORIES - carbs_now * 4 - fats_now * 9) / 4;

            std::vector<double> result = find_solution(breakfasts[id1], lunches[id2], dinners[id3], carbs_now, fats_now, prots_now);

            if (result.size() == 3 && is_good_solution(breakfasts[id1] * result[0], lunches[id2] * result[1], dinners[id3] * result[2])) {
                Menu menu = breakfasts[id1] + lunches[id2] + dinners[id3];
                if (menu.quality > max_quality) {
                    max_quality = menu.quality;
                }
            }
        }
    }
    int time_end = clock();
    return std::make_pair(max_quality, time_end - time_start);
}

int main() {
    std::vector<Recipe> breakfasts = read_recipes_from_file("data/breakfast.txt");
    std::vector<Recipe> lunches = read_recipes_from_file("data/lunch.txt");
    std::vector<Recipe> dinners = read_recipes_from_file("data/dinner.txt");

    // exp for fixed carbs, fats, prots
    /*
    for (int amount = 1000; amount <= 1000; amount += 1000) {
        std::vector<std::pair<int, int> > results;
        for (int i = 0; i < 100; i++) {
            std::pair<int, int> result = linear_exp(breakfasts, lunches, dinners, amount);
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
    */

    // exp for random carbs, fats, prots
    for (int amount = 10; amount <= 100; amount += 10) {
        std::vector<std::pair<int, int> > results;
        for (int i = 0; i < 100; i++) {
            std::pair<int, int> result = linear_exp_random_balance(breakfasts, lunches, dinners, 1000, amount);
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
