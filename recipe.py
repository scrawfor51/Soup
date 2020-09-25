from ingredient import Ingredient
import random


def ingredients_from_file(filename):
    ingredients = []
    with open(filename) as file:
        for line in file:
            divided_line = line.split(" ", 2)
            ounces = float(divided_line[0])
            name = divided_line[2]
            ingredients.append(Ingredient(ounces, name))

    return ingredients


class Recipe:
    """
    A class representing a recipe.

    Attributes
    ----------
    ingredients : list of Ingredient
        the ingredients in the recipe

    Methods
    -------
    add_ingredient(self, ingredient):
        Adds an ingredient to the recipe.

    fitness(self):
        Returns the fitness of the recipe.
    """
    master_ingredients = set()  # static variable for all ingredients

    def __init__(self, ingredients):
        """Construct a recipe from a given filename"""
        self.ingredients = ingredients
        self.master_ingredients.update([ingredient.name for ingredient in ingredients])

    def __repr__(self):
        """Return a string representation of the recipe; inverse of __init__"""
        string = ""
        for ingredient in self.ingredients:
            string += str(ingredient)

        return string

    def add_ingredient(self, ingredient):
        """Add the given ingredient"""
        self.ingredients.append(ingredient)

    def fitness(self):
        """Return the fitness i.e. the length of the recipe"""
        return len(self.ingredients)

    def change_amount(self):
        """Helper function for the mutate function, changes the amount of an ingredient uniformly selected at random."""
        item = random.choice(self.ingredients)
        item.set_amount(item.ounces + round(random.uniform(0, item.ounces), 2))

    def change_ingredient(self):
        """Helper function for the mutate function, changes an ingredient uniformly selected at random."""
        item = random.choice(self.ingredients)
        item.set_name(random.choice(tuple(self.master_ingredients)))

    def add_ingredient(self):
        """Helper function for the mutate function, adds an ingredient uniformly selected at random."""
        # ensures that we don't break the program if all the ingredients are in a recipe
        if len(self.ingredients) == len(self.master_ingredients):
            return

        ingredient_names = [ingredient.name for ingredient in self.ingredients]

        # take the difference between the master set and this recipe's names
        new_ingredient_name = random.choice(tuple(self.master_ingredients - set(ingredient_names)))
        self.ingredients.append(Ingredient(round(random.uniform(0, 16), 2), new_ingredient_name))

    def delete_ingredient(self):
        """Helper function for the mutate function, deletes an ingredient uniformly selected at random."""
        self.ingredients.pop(random.randint(0, self.fitness() - 1))

    def mutate(self):
        """Takes a recipe in list form and mutates it in some way."""
        possible_mutations = [self.change_amount,
                              self.change_ingredient,
                              self.add_ingredient,
                              self.delete_ingredient]

        random.choice(possible_mutations)()

    def normalize(self):
        """Takes a list of ingredients and normalizes them to equal 100oz."""
        original_sum = sum([ingredient.ounces for ingredient in self.ingredients])
        scaling_factor = 1

        if original_sum != 0:
            scaling_factor = 100 / original_sum  # gives us the amount to multiply our entries by to scale to 100 oz

        for item in self.ingredients:
            amount = round(item.ounces * scaling_factor, 2)

            # don't let amounts fall below 0.01
            if amount < 0.01:
                amount = 0.01

            item.set_amount(amount)

    def deduplicate(self):
        """Remove duplicates which can occur during crossover"""
        unique_items = []

        for item in self.ingredients:
            if item.name not in unique_items:
                unique_items.append(item)

        self.ingredients = unique_items

