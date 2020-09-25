# Soupoholics PQ1 - Simplified Pierre Soup 

### A CSCI 3725 Project by Stephen Crawford, Gerard Goucher, and Sam Roussel

#### Setting up our project

Our project utilizes the Glob, OS, and Random modules, which both come pre-packaged with Python distributions, 
so just make sure that you have Python version 3.7 or later installed.

Then, simply run the main.py script in the terminal by navigating to our project folder,
and running the following command:

    $ python3 main.py <number of generations desired>
    
 ## Project Description
 
 Our project utilizes a variety of different Python features and modules to 
 implement the simplified PIERRE soup model. We three classes, our Ingredient class, our Recipe class and our main
 class. 
 
 The Ingredient class is used to store ingredient information, name and ounces. The Recipe class stores ingredients in 
 the recipe, an external representation function, a fitness determination function, and a globally accessible file
 reader method.
 
 The main class contains the bulk of our process. We first use the glob module to access our inputted recipes and make 
 Recipe objects out of them. Afterwords, we iterate through each one and append any new ingredients to a global variable 
 later accessed by the mutation function. 
 
 Following this, we create new recipes using the fill_generation function. This function uses several helper methods to 
 do this process, first sorting the recipes by their fitness, and then selecting two recipes based on probability
 proportional to their fitness using the recipe_select function.
 
 After this, new recipes are generated utilizing the gen_soup function. Here, a new recipe is created by combining one 
 part from each inputted recipe, both split in two at a randomly selected pivot point. From here, new recipes are mutated
 using the mutate function.
 
 The mutate function randomly uniformly calls one of four mutation functions. The possibilities are: ingredient amounts 
 are changed, ingredients are added, ingredients are deleted, or ingredients are switched out for another. 
 After one of the four possible mutations are done, we call the normalize function to make our new recipes have 100oz of
 ingredients. Then, our new soup recipes are returned in our gen_soup function and in our fill_generation function!
 
 With our new recipes, and back to the main function, we call the select_new_generation function with the population of 
 our old and new soups, take the top 50% most fit recipes from both, and return our final soup recipes, writing them in
 our output files.  
    
 ## Sources
 
 Please note that the following sources were utilized to create our project:
 
 [W3schools](https://www.w3schools.com/python/ref_dictionary_pop.asp#:~:text=The%20pop()%20method%20removes,()%20method%2C%20see%20example%20below.),
 this source was utilized to discover the python array pop() method.
 
 
