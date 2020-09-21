import glob
import os
from recipe import Recipe


def main():
    recipes = []

    # read the text recipes into a list of Recipe objects
    for filename in glob.glob("resources/input/*.txt"):
        recipes.append(Recipe(filename))

    # for each generation
        # create n new individuals, where n is the population size
            # select two individuals from the population (probability based on fitness)
            # perform crossover
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
