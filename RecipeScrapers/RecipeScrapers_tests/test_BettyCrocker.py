import unittest
import bs4 as bs
import os
from .TestHelpers import read_recipe_data, read_empty_recipe_data
from RecipeScrapers import BettyCrockerScraper


class BettyCrockerScrapperTestClass(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        self.recipeData = ''

    def test_recipe_name_get_correct_name(self):

        self.recipeData = read_recipe_data(BettyCrockerScraper, 'bettyCrockerTest1.html')
        actualName = 'Stuffed Peppers'
        testName = self.recipeData['name']
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))

    def test_recipe_name_name_not_found(self):

        actualName = ''
        self.recipeData = read_empty_recipe_data(BettyCrockerScraper)
        testName = self.recipeData['name']
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))

    def test_recipe_ingredients_gets_correct_ingredients(self):

        self.recipeData = read_recipe_data(BettyCrockerScraper, 'bettyCrockerTest1.html')
        actualIngredients = ['4 large bell peppers (any color)',
                             '1 lb lean (at least 80%) ground beef',
                             '2 tablespoons chopped onion',
                             '1 cup cooked rice',
                             '1 teaspoon salt',
                             '1 clove garlic, finely chopped',
                             '1 can (15 oz) Muir Glen™ organic tomato sauce',
                             '3/4 cup shredded mozzarella cheese (3 oz)']
        actualIngredientsStr = ''
        for recipe_instruction_item in actualIngredients:
            actualIngredientsStr += '{}\n'.format(recipe_instruction_item.strip())
        testIngredients = self.recipeData['recipeIngredient']
        self.assertTrue(isinstance(testIngredients, str), 'Ingredients should be a list')
        self.assertEqual(actualIngredientsStr, testIngredients, 'Recipe Ingredient Mismatch')

    def test_recipe_ingredients_ingredients_not_found(self):

        self.recipeData = read_empty_recipe_data(BettyCrockerScraper)

        actualIngredientsStr = ''
        testIngredients = self.recipeData['recipeIngredient']
        self.assertTrue(isinstance(testIngredients, str), 'Ingredients should be a string')
        self.assertEqual(actualIngredientsStr, testIngredients, 'Recipe Ingredient Mismatch')

    def test_recipe_instructions(self):

        self.recipeData = read_recipe_data(BettyCrockerScraper, 'bettyCrockerTest1.html')
        testInstructions = self.recipeData['recipeInstructions']
        self.assertTrue(isinstance(testInstructions, str), 'Recipe Instructions should be a string')

    def test_recipe_instructions_not_found(self):

        self.recipeData = read_empty_recipe_data(BettyCrockerScraper)
        expectedInstructions = ''
        testInstructions = self.recipeData['recipeInstructions']
        self.assertEqual(expectedInstructions, testInstructions)

    def test_recipe_image_url_found(self):

        self.recipeData = read_recipe_data(BettyCrockerScraper, 'bettyCrockerTest1.html')
        expected_image_url = 'https://images-gmi-pmc.edge-generalmills.com/3512d6fb-41d3-41e7-a66d-f234a5942b6a.jpg'
        self.assertEqual(self.recipeData['image'], expected_image_url)

    def test_recipe_image_url_not_found(self):

        self.recipeData = read_empty_recipe_data(BettyCrockerScraper)
        expected_image_url = ''
        self.assertEqual(self.recipeData['image'], expected_image_url)
