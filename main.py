import glob
import os
from recipe import Recipe, ingredients_from_file
import random

master_ingredients = []  # global variable accessible for mutation methods

# Gen new recipe name based off ingredients
def newName(new_recipe):
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


# sort recipes by fitness
# @param recipes -- the list of recipes in our population
# @ param lowRecipeIndex -- the low index
# @param highRecipeIndex -- the high index
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


def quicksortForSoup(recipes, lowRecipeIndex, highRecipeIndex):
    if len(recipes) <= 1:
        return recipes

    if lowRecipeIndex < highRecipeIndex:

        partitionIndex = quicksortPartition(recipes, lowRecipeIndex, highRecipeIndex)

        quicksortForSoup(recipes, lowRecipeIndex, partitionIndex - 1)
        quicksortForSoup(recipes, partitionIndex + 1, highRecipeIndex)


def pivotIndex(recipe):
    recipeLen = recipe.fitness()
    randPiv = random.randint(0, recipeLen - 1)
    return randPiv

def recipeSelect(recipes):
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



def fillGeneration(recipes):
    newGen = []

    recipes = recipes
    quicksortForSoup(recipes, 0, len(recipes) - 1)

    while len(newGen) < (len(recipes)/2):
        s1 = recipeSelect(recipes)
        s2 = recipeSelect(recipes)
        newGen += genSoup(s1, s2)

    return newGen


def genSoup(recipe_1, recipe_2):

    newSoups = []

    soup_1_pivot = pivotIndex(recipe_1)
    soup_2_pivot = pivotIndex(recipe_2)

    soup_1_part_1 = recipe_1.ingredients[0 : soup_1_pivot]
    soup_1_part_2 = recipe_1.ingredients[soup_1_pivot: ]

    soup_2_part_1 = recipe_2.ingredients[0 : soup_2_pivot]
    soup_2_part_2 = recipe_2.ingredients[soup_2_pivot : ]

    new_recipe_1 = mutate(soup_1_part_1 + soup_2_part_1)
    new_recipe_2 = mutate(soup_1_part_2 + soup_2_part_2)

    newSoups.append(Recipe(soup_1_part_1 + soup_2_part_1))
    newSoups.append(Recipe(soup_1_part_2 + soup_2_part_2))

    return newSoups


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

    # print(string_arr[index_to_change])
    # print(master_ingredients[new_ingredient])

    string_arr[index_to_change].name = master_ingredients[new_ingredient]


def mutate(string_arr):
    """Takes a recipe in list form and mutates it in some way."""

    mutate_op = 2#random.randrange(0, 4) #used to determine which mutation will occur
    # print(string_arr)
    if mutate_op == 0:
        change_amt(string_arr)
    elif mutate_op == 1:
        change_ingredient(string_arr)
    # print(string_arr)
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


    fillGeneration(recipes)

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
