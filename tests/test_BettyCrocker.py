import unittest
import bs4 as bs

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from WebsiteScraper import BettyCrockerScrapper

class KitchenScrapperTestClass(unittest.TestCase):


    @classmethod
    def setUpClass(self):
         with open(os.path.join(os.path.dirname(__file__),'testHtml/bettyCrockerTest1.html'),'r') as inHtml:
            soup = bs.BeautifulSoup(inHtml.read(), 'lxml')
            self.recipeData = BettyCrockerScrapper().ExtractRecipeData(soup)

    def test_RecipeName(self):

        actualName = 'Bacon-Wrapped Asparagus'
        testName = self.recipeData['name']
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))


    def test_RecipeIngredients(self):

        actualIngredients = ['2 tablespoons butter, melted',
                             '1/4 teaspoon crushed red pepper flakes',
                             '1 lb fresh asparagus spears, trimmed',
                             '8 slices bacon',
                             '1 lemon, cut in wedges']
        testIngredients = self.recipeData['recipeIngredient']
        self.assertTrue(isinstance(testIngredients, list), 'Ingredients should be a list')
        self.assertEqual(actualIngredients, testIngredients, 'Recipe Ingredient Mismatch')


    def test_RecipeInstructions(self):

        testInstructions = self.recipeData['recipeInstructions']
        self.assertTrue(isinstance(testInstructions, str), 'Recipe Instructions should be a string')
