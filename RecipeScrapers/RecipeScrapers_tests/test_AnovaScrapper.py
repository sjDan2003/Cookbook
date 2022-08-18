import unittest
import bs4 as bs
import os
from RecipeScrapers import JsonScraper


class AnovaScrapperScrapperTestClass(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        self.recipeData = ''

    def read_recipe_data(self):
        """
            Helper function to read the actual recipe from a test HTML file
            This function will open the file, creat a soup object from it
            and call the recipe scraper to extract the data.
        """

        with open(os.path.join(os.path.dirname(__file__),'testHtml/test_Anova.html'), 'r') as in_html:
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
        actualName = 'Sous Vide Carnitas Tacos'
        testName = self.recipeData['name']
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))

    def test_recipe_name_name_not_found(self):

        actualName = ''
        self.read_empty_recipe_data()
        testName = self.recipeData['name']
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))

    def test_recipe_ingredients(self):

        self.read_recipe_data()
        actual_ingredients = ["1 1/2 pounds pork shoulder or country-style pork ribs, cut into 1-inch cubes",
                              "1/2 medium onion, peeled",
                              "1 tablespoon lime juice",
                              "1 teaspoon kosher salt",
                              "1/2 teaspoon cumin",
                              "1/2 teaspoon dried oregano",
                              "1 bay leaf",
                              "1/2 orange",
                              "Small corn tortillas, for serving",
                              "Fresh cilantro leaves, for serving ",
                              "Chopped white onion, for serving",
                              "Thinly sliced red radishes, for serving",
                              "Lime wedges, for serving"]
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
