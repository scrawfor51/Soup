import glob
from operator import methodcaller
import os
import random
from recipe import Recipe, ingredients_from_file
import sys


def recipe_select(recipes):
    """
    Selects a recipe, using the fitness as the weight in random.choices.

    @param recipes -- A list of the different soup recipes in the population.
    @return the selected recipe
    """
    fitness_list = [recipe.fitness() for recipe in recipes]
    return random.choices(recipes, weights=fitness_list)[0]


def fill_generation(recipes):
    """
    This is a helper function which takes in the total list of recipes and calls for new recipes to be made so long as
    the new population is less then the starting population.

    @param recipes -- A list of the different soup recipes in the population.
    @return A new generation of the soup population which is equal in size to the starting population but consists of
    new soup recipes.
    """
    generation = []

    # generate n recipes, where n is our current population
    for i in range(len(recipes)):
        soup_one = recipe_select(recipes)
        soup_two = recipe_select(recipes)
        generation.append(gen_soup(soup_one, soup_two))

    return generation


def gen_soup(recipe_one, recipe_two):
    """
    This function takes in two existing soup recipes and randomly splits the soups at an pivot index.
    It then combines the halves of the two different soups so a new soup is created.

    @param recipe_one the first soup we are using as a base for the new recipes.
    @param recipe_two the second soup we are using as a base for the new recipes.
    @return the new soup
    """
    pivot_one = random.randint(0, recipe_one.fitness() - 1)
    pivot_two = random.randint(0, recipe_two.fitness() - 1)

    soup = Recipe(recipe_one.ingredients[0: pivot_one] + recipe_two.ingredients[pivot_two:])
    soup.mutate()
    soup.deduplicate()
    soup.normalize()

    return soup


def select_new_generation(population_one, population_two):
    """
    Takes in the last population and the new population, sorts them by fitness, and then uses the ordering to select
    the three fittest recipes from each population and combine them into a new generation. At this point, the three
    least fit soups from each generation can be discarded, and the new generation sent forth as the new starting
    population for the next generation of soup recipes.

    @param population_one -- The oldest population of soup, already sorted by fitness
    @param population_two -- The younger population of soup, sorted by fitness
    @return A new population of soup comprised of the three fittest recipes from each of the two populations
    """
    population_one.sort(key=methodcaller("fitness"))
    population_two.sort(key=methodcaller("fitness"))

    return population_one[3:] + population_two[3:]


def main():
    recipes = []

    # read the text recipes into a list of Recipe objects
    for filename in glob.glob("resources/input/*.txt"):
        recipes.append(Recipe(ingredients_from_file(filename)))

    # get number of generations from command line; default to 10
    if len(sys.argv) > 1:
        num_generations = int(sys.argv[1])
    else:
        num_generations = 10

    # evolve our recipes
    for i in range(num_generations):
        new_recipes = fill_generation(recipes)
        new_population = select_new_generation(recipes, new_recipes)

    # create our output file
    os.makedirs("output", exist_ok=True)

    # output the generated recipes to text files
    for i in range(len(recipes)):
        with open("output/new_recipe_" + str(i) + ".txt", "w") as file:
            file.write(str(new_population[i]))


if __name__ == "__main__":
    main()
