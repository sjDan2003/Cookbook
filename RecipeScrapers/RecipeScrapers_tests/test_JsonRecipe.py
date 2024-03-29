import unittest
import bs4 as bs
import os
from RecipeScrapers import JsonScraper


class JsonScrapperScrapperTestClass(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        self.recipeData = ''

    def read_recipe_data(self):
        """
            Helper function to read the actual recipe from a test HTML file
            This function will open the file, creat a soup object from it
            and call the recipe scraper to extract the data.
        """

        with open(os.path.join(os.path.dirname(__file__),'testHtml/test_JsonTest2.html'), 'r') as in_html:
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
        actualName = 'Pork Tenderloin Rub'
        testName = self.recipeData['name']
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))

    def test_recipe_name_name_not_found(self):

        actualName = ''
        self.read_empty_recipe_data()
        testName = self.recipeData['name']
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))

    def test_recipe_ingredients(self):

        self.read_recipe_data()
        actual_ingredients = ["1 teaspoon garlic powder",
                             "1 teaspoon dried oregano",
                             "1 teaspoon ground cumin",
                             "1 teaspoon ground coriander",
                             "1/2 teaspoon ground thyme",
                             "1 teaspoon salt",
                             "About 1 1/4 pounds pork tenderloin (This is where we buy our favorite pork tenderloin.*)",
                             "1 tablespoon olive oil or avocado oil"]
        actual_ingredients_str = ''
        for recipe_instruction_item in actual_ingredients:
            actual_ingredients_str += '{}\n'.format(recipe_instruction_item.strip())
        testIngredients = self.recipeData['recipeIngredient']
        self.assertTrue(isinstance(testIngredients, str), 'Ingredients should be a list')
        self.assertEqual(actual_ingredients_str, testIngredients, 'Recipe Ingredient Mismatch')

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
