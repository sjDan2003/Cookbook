import unittest
import bs4 as bs
import os
from RecipeScrapers import JsonScraper


class FoodNetworkScrapperTestClass(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        self.recipeData = ''

    def read_recipe_data(self):
        """
            Helper function to read the actual recipe from a test HTML file
            This function will open the file, creat a soup object from it
            and call the recipe scraper to extract the data.
        """

        with open(os.path.join(os.path.dirname(__file__),'testHtml/foodNetworkTest1.html'), 'r') as in_html:
            soup = bs.BeautifulSoup(in_html.read(), 'lxml')
            self.recipeData = JsonScraper().extract_recipe_data(soup)

    def read_empty_recipe_data(self):
        """
            Helper function to parse an empty HTML string
            This will be used to test the case where recipe data
            is not found.
        """

        soup = bs.BeautifulSoup("<html></html>", 'lxml')
        self.recipeData = JsonScraper().extract_recipe_data(soup)

    def test_recipe_name_get_correct_name(self):

        self.read_recipe_data()
        actualName = 'Perfect Turkey Burgers'
        testName = self.recipeData['name']
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))

    def test_recipe_name_name_not_found(self):

        actualName = ''
        self.read_empty_recipe_data()
        testName = self.recipeData['name']
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))

    def test_recipe_ingredients(self):

        self.read_recipe_data()
        actualIngredients = ['1 large portobello mushroom cap',
                             '1 tablespoon coarsely chopped shallot',
                             '3 tablespoons lightly packed fresh parsley',
                             '1 1/4 pounds 85% to 93% lean ground turkey',
                             '2 tablespoons extra-virgin olive oil, plus more for brushing',
                             '1 teaspoon Worcestershire sauce',
                             'Kosher salt and freshly ground pepper',
                             '8 thin slices manchego or white cheddar cheese',
                             '4 English muffins, split',
                             'Dijon mustard, mayonnaise and sliced avocado, for topping']
        actualIngredientsStr = ''
        for recipe_instruction_item in actualIngredients:
            actualIngredientsStr += '{}\n'.format(recipe_instruction_item.strip())
        testIngredients = self.recipeData['recipeIngredient']
        self.assertTrue(isinstance(testIngredients, str), 'Ingredients should be a list')
        self.assertEqual(actualIngredientsStr, testIngredients, 'Recipe Ingredient Mismatch')

    def test_recipe_ingredients_ingredients_not_found(self):

        self.read_empty_recipe_data()

        actualIngredientsStr = ''
        testIngredients = self.recipeData['recipeIngredient']
        self.assertTrue(isinstance(testIngredients, str), 'Ingredients should be a string')
        self.assertEqual(actualIngredientsStr, testIngredients, 'Recipe Ingredient Mismatch')

    def test_recipe_instructions(self):

        self.read_recipe_data()
        testInstructions = self.recipeData['recipeInstructions']
        self.assertTrue(isinstance(testInstructions, str), 'Recipe Instructions should be a string')
