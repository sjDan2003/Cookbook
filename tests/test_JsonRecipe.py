import unittest
import bs4 as bs
import os
from WebsiteScraper import JsonScrapper


class JsonScrapperScrapperTestClass(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        with open(os.path.join(os.path.dirname(__file__),'testHtml/foodNetworkTest1.html'),'r') as inHtml:
            soup = bs.BeautifulSoup(inHtml.read(), 'lxml')
            self.recipeData = JsonScrapper().ExtractRecipeData(soup)

    def test_RecipeName(self):

        actualName = 'Perfect Turkey Burgers'
        testName = self.recipeData['name']
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))

    def test_RecipeIngredients(self):

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
        testIngredients = self.recipeData['recipeIngredient']
        self.assertTrue(isinstance(testIngredients, list), 'Ingredients should be a list')
        self.assertEqual(actualIngredients, testIngredients, 'Recipe Ingredient Mismatch')

    def test_RecipeInstructions(self):

        testInstructions = self.recipeData['recipeInstructions']
        self.assertTrue(isinstance(testInstructions, str), 'Recipe Instructions should be a string')
