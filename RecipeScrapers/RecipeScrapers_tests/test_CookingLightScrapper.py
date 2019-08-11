import unittest
import bs4 as bs
import os
from RecipeScrapers import CookingLightScraper


class CookingLightScrapperTestClass(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        with open(os.path.join(os.path.dirname(__file__), 'testHtml/cookingLightTest1.html'), 'r') as inHtml:
            soup = bs.BeautifulSoup(inHtml.read(), 'lxml')
            self.recipeData = CookingLightScraper().extract_recipe_data(soup)

    def test_recipe_name(self):

        actualName = 'Fluffiest Multigrain Pancakes with Almond Butter Drizzle'
        testName = self.recipeData['name']
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))

    def test_recipe_ingredients(self):

        actualIngredients = ['2/3 cup old-fashioned oats',
                             '1 1/3 cups nonfat buttermilk',
                             '1/4 cup warm water',
                             '1/4 cup natural almond butter',
                             '2 1/2 tablespoons maple syrup, divided',
                             '3 ounces white whole-wheat flour (about 3/4 cup)',
                             '2 teaspoons baking powder',
                             '1/4 teaspoon baking soda',
                             '1/4 teaspoon kosher salt',
                             '1 teaspoon vanilla extract',
                             '1  large egg, lightly beaten',
                             '1 1/3 cups fresh raspberries']
        testIngredients = self.recipeData['recipeIngredient']
        self.assertTrue(isinstance(testIngredients, list), 'Ingredients should be a list')
        self.assertEqual(actualIngredients, testIngredients, 'Recipe Ingredient Mismatch')

    def test_recipe_instructions(self):

        testInstructions = self.recipeData['recipeInstructions']
        self.assertTrue(isinstance(testInstructions, str), 'Recipe Instructions should be a string')
