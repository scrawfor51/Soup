import glob
import os
from recipe import Recipe, ingredients_from_file
import random
from operator import methodcaller


# Gen new recipe name based off ingredients
def new_name(new_recipe):
    name = ""
    soup_type = ""
    for ingredient in new_recipe:
        name += ingredient + "-y "
    if "seafood" & "milk" in new_recipe:
        soup_type = "bisque"
    if "cold" in new_recipe:
        soup_type = "gazpacho"
    if "ground" in new_recipe:
        soup_type = "consomme"
    if "flour" | "cornstarch" in new_recipe:
        soup_type = "thick"
    if "mush" in new_recipe:
        soup_type = "pottage"
    return name + soup_type


def recipe_select(recipes):
    fitness_list = [recipe.fitness() for recipe in recipes]
    return random.choices(recipes, weights=fitness_list)[0]


def fill_generation(recipes):
    generation = []

    # sort recipes by fitness
    recipes.sort(key=methodcaller("fitness"))

    # there are two "offspring" for each pair of parents
    for i in range(0, len(recipes) // 2):
        soup_one = recipe_select(recipes)
        soup_two = recipe_select(recipes)
        generation += gen_soup(soup_one, soup_two)

    return generation


def gen_soup(recipe_one, recipe_two):
    new_soups = []
    pivot_one = random.randint(0, recipe_one.fitness() - 1)
    pivot_two = random.randint(0, recipe_two.fitness() - 1)

    soup_one_begin = recipe_one.ingredients[0: pivot_one]
    soup_one_end = recipe_one.ingredients[pivot_one:]

    soup_two_begin = recipe_two.ingredients[0: pivot_two]
    soup_two_end = recipe_two.ingredients[pivot_two:]

    new_soups.append(Recipe(soup_one_begin + soup_two_end))
    new_soups.append(Recipe(soup_two_begin + soup_one_end))

    return new_soups


def main():
    recipes = []

    # read the text recipes into a list of Recipe objects
    for filename in glob.glob("resources/input/*.txt"):
        recipes.append(Recipe(ingredients_from_file(filename)))

    new_gen = fill_generation(recipes)

    # perform mutation
    # normalize the new individuals to 100 ounces
    # select the fittest half of the new generation and the previous generation, deleting the rest

    # set this to our end population
    population = new_gen

    os.makedirs("output", exist_ok=True)

    # output the generated recipes to text files
    for i in range(len(population)):
        with open("output/new_recipe_" + str(i) + ".txt", "w") as file:
            file.write(str(population[i]))


if __name__ == "__main__":
    main()
