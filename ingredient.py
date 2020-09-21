class Ingredient:
    """
    A class representing an ingredient.

    Attributes
    ----------
    ounces : float
        the amount of the ingredient

    name : str
        the name of the ingredient

    Methods
    -------
    set_amount(self, ounces):
        sets the amount in ounces

    set_name(self, name):
        sets the name

    """
    def __init__(self, ounces, name):
        """Construct an ingredient by amount and name"""
        self.ounces = ounces
        self.name = name

    def __repr__(self):
        """Return the ingredient as a string of form: [amount] oz [name]"""
        return str(self.ounces) + " oz " + self.name

    def set_amount(self, ounces):
        """Set the number of ounces"""
        self.ounces = ounces

    def set_name(self, name):
        """Set the name"""
        self.name = name
