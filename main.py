import glob
import os
from recipe import Recipe
import random


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

    print (soup_2_part_1)
    newSoups += Recipe(soup_1_part_1 + soup_2_part_1)
    newSoups += Recipe(soup_1_part_2 + soup_2_part_2)

    return newSoups


def main():
    recipes = []

    # read the text recipes into a list of Recipe objects
    for filename in glob.glob("resources/input/*.txt"):
        recipes.append(Recipe(filename))

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
