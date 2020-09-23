from ingredient import Ingredient


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

    def __init__(self, ingredients):
        """Construct a recipe from a given filename"""
        self.ingredients = ingredients

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
