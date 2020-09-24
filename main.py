import glob
import os
from recipe import Recipe, ingredients_from_file
from ingredient import Ingredient
import random

master_ingredients = []  # global variable accessible for mutation methods

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

# Code credit of geeksforgeeks.com all intellectual property and credit belongs to the authors of the website and the code's
# original author Mohit Kumra. The code was adapted to fit our purposes but still originated from the original author.


""" sort recipes by fitness
@param recipes -- the list of recipes in our population
@ param lowRecipeIndex -- the low index
@param highRecipeIndex -- the high index
"""

def quicksortPartition(recipes, lowRecipeIndex, highRecipeIndex):
    lesserIndex = lowRecipeIndex - 1
    pivot = recipes[highRecipeIndex].fitness()

    for recipe in range (lowRecipeIndex, highRecipeIndex):

        if recipes[recipe].fitness() <= pivot:

            lesserIndex += 1
            temp = recipes[lesserIndex]
            recipes[lesserIndex] = recipes[recipe]
            recipes[recipe] = temp

    temp = recipes[lesserIndex + 1]
    recipes[lesserIndex + 1] = recipes[highRecipeIndex]
    recipes[highRecipeIndex] = temp
    return lesserIndex + 1


def sort_soup(recipes, lowRecipeIndex, highRecipeIndex):
    if len(recipes) <= 1:
        return recipes

    if lowRecipeIndex < highRecipeIndex:

        partitionIndex = quicksortPartition(recipes, lowRecipeIndex, highRecipeIndex)

        sort_soup(recipes, lowRecipeIndex, partitionIndex - 1)
        sort_soup(recipes, partitionIndex + 1, highRecipeIndex)


"""
This method takes in a recipe and then randomly selects a point within that recipe which will act as its internal pivot.
The pivot is later used when partitioning the soup into seperate halves which are recombined with another soups' halves
to create a pair of entirely new soup recipes. 

@param recipe -- The soup recipe we want to randomly partition. 
@return a random pivot index within the soup recipe.
"""
def pivot_index(recipe):
    recipeLen = recipe.fitness()
    rand_pivot = random.randint(0, recipeLen - 1)
    return rand_pivot


"""
This method takes in an array of recipes and then pseudo-randomly, selects one of them. The process of selecting them
is based off of their relative fitness' where the most fit recipe is given the highest odds of being selected. 

It is important that the passed list is already sorted by fitness. 

@param recipes -- A sorted array of soup recipes where the recipes are ordered based on their relative fitness.
return a pseudo-randomly selected soup from the provided list. 
"""
def recipe_select(recipes):
    selectorNumber = random.randint(0, 20)
    if selectorNumber < 5:
        return recipes[5]
    if selectorNumber > 5 & selectorNumber < 10:
        return recipes[4]
    if selectorNumber > 10 & selectorNumber < 14:
        return recipes[3]
    if selectorNumber > 14 & selectorNumber < 17:
        return recipes[2]
    if selectorNumber > 17 & selectorNumber < 19:
        return recipes[1]
    else:
        return recipes[0]


"""
This is a helper function which takes in the total list of recipes and calls for new recipes to be made so long as the new
population is less then the starting population. 

It uses the sort_soup, recipe_select, and gen_soup methods to facillitate the generation creation. 

@param recipes -- A list of the different soup recipes in the population.
@return A new generation of the soup population which is equal in size to the starting population but consists of new 
soup recipes. 
"""
def fill_generation(recipes):
    new_gen = []

    recipes = recipes
    sort_soup(recipes, 0, len(recipes) - 1)

    while len(new_gen) < (len(recipes)/2):
        s1 = recipe_select(recipes)
        s2 = recipe_select(recipes)
        new_gen += gen_soup(s1, s2)

    return new_gen


"""
This function takes in two existing soup recipes and uses the helper method pivot_index to randomly split the 
soups at an inex. It then combines the halves of the two different soups (i.e. half 1 and half 2) so that two new soups 
are created. 

@param recipe_1 the first soup we are using as a base for the new recipes.
@param recipe_2 the second soup we are using as a base for the new recipes.
@return An array consiting of two soup recipes. 
"""
def gen_soup(recipe_1, recipe_2):

    new_soups = []

    soup_1_pivot = pivot_index(recipe_1)
    soup_2_pivot = pivot_index(recipe_2)

    soup_1_part_1 = recipe_1.ingredients[0 : soup_1_pivot]
    soup_1_part_2 = recipe_1.ingredients[soup_1_pivot: ]

    soup_2_part_1 = recipe_2.ingredients[0 : soup_2_pivot]
    soup_2_part_2 = recipe_2.ingredients[soup_2_pivot : ]

    new_recipe_1 = mutate(soup_1_part_1 + soup_2_part_1)
    new_recipe_2 = mutate(soup_1_part_2 + soup_2_part_2)

    new_soups.append(Recipe(new_recipe_1))#soup_1_part_1 + soup_2_part_1))
    new_soups.append(Recipe(new_recipe_2))#soup_1_part_2 + soup_2_part_2))

    return new_soups



def change_amt(string_arr):
    """Helper function for the mutate function, changes the amount of an ingredient uniformly selected at random."""

    index_to_change = random.choice(range(len(string_arr)))
    change_holder = string_arr[index_to_change].ounces  # holds original value

    addition = round(random.uniform(0, change_holder), 2)  # the value we will add to our our current ingredient amount
    # chosen randomly from 0 to the original ingredient value

    string_arr[index_to_change].set_amount(change_holder + addition)


def change_ingredient(string_arr):
    """Helper function for the mutate function, changes an ingredient uniformly selected at random."""

    index_to_change = random.choice(range(len(string_arr)))
    new_ingredient = random.choice(range(len(master_ingredients)))

    string_arr[index_to_change].name = master_ingredients[new_ingredient]


def add_ingredient(string_arr):
    """Helper function for the mutate function, adds an ingredient uniformly selected at random."""

    name_storage = []
    for ingredient in string_arr:
        name_storage.append(ingredient.name)

    if len(name_storage) == len(master_ingredients):  # ensures that we don't break the program if all the ingredients
        # are in a recipe
        return

    new_ingredient = random.choice(range(len(master_ingredients)))

    while True:  # loop to ensure that we're not adding an ingredient we already have
        if not master_ingredients[new_ingredient] in name_storage:
            break
        else:
            new_ingredient = random.choice(range(len(master_ingredients)))

    new_amt = round(random.uniform(0, 16), 2)

    string_arr.append(Ingredient(new_amt, master_ingredients[new_ingredient]))


def delete_ingredient(string_arr):
    """Helper function for the mutate function, deletes an ingredient uniformly selected at random."""

    index_to_delete = random.choice(range(len(string_arr)))
    string_arr.pop(index_to_delete)  # pop method discovered on w3schools.com

def mutate(string_arr):
    """Takes a recipe in list form and mutates it in some way."""

    mutate_op = random.randrange(0, 4) #used to determine which mutation will occur

    if mutate_op == 0:
        change_amt(string_arr)
    elif mutate_op == 1:
        change_ingredient(string_arr)
    elif mutate_op == 2:
        add_ingredient(string_arr)
    else:
        delete_ingredient(string_arr)

    return

def main():
    recipes = []

    # read the text recipes into a list of Recipe objects
    for filename in glob.glob("resources/input/*.txt"):
        recipes.append(Recipe(ingredients_from_file(filename)))

    for recipe in recipes:  # allowing us to make a master list of ingredients to mutate from
        for ingredient in recipe.ingredients:

            if not ingredient.name[:-1] in master_ingredients:
                master_ingredients.append(ingredient.name[:-1])

    fill_generation(recipes)

        # create n new individuals, where n is the population size

            # select two individuals from the population (probability based on fitness)


            # perform mutation
        # normalize the new individuals to 100 ounces
        # select the fittest half of the new generation and the previous generation, deleting the rest

    os.makedirs("output", exist_ok=True)

    # output the generated recipes to text files
    for i in range(len(recipes)):
        with open("output/new_recipe_" + str(i) + ".txt", "w") as file:
            file.write(str(recipes[i]))





if __name__ == "__main__":
    main()
