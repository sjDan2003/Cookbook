import unittest
import bs4 as bs

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from WebsiteScraper import CooksScrapper

class KitchenScrapperTestClass(unittest.TestCase):


    @classmethod
    def setUpClass(self):
         with open(os.path.join(os.path.dirname(__file__),'testHtml/cooksTest1.html'),'r') as inHtml:
            soup = bs.BeautifulSoup(inHtml.read(), 'lxml')
            self.recipeData = CooksScrapper().ExtractRecipeData(soup)

    def test_RecipeName(self):

        actualName = 'Genuine Virginia Baked Ham'
        testName = self.recipeData['name']
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))


    def test_RecipeIngredients(self):

        actualIngredients = ['1 small, rather lean ham',
                             '6 cloves',
                             '1/2 teaspoonful celery seed',
                             '2 tablespoonful sugar',
                             'Boiling water',
                             '1 egg, beaten',
                             '10 peppercorns',
                             '1/2 teaspoonful ground cinnamon',
                             '1 quart sweet cider',
                             '2 tablespoonfuls breadcrumbs',
                             'Celery leaves and curls for garnish',
                             'Currant sauce']
        testIngredients = self.recipeData['recipeIngredient']
        self.assertTrue(isinstance(testIngredients, list), 'Ingredients should be a list')
        self.assertEqual(actualIngredients, testIngredients, 'Recipe Ingredient Mismatch')


    def test_RecipeInstructions(self):

        testInstructions = self.recipeData['recipeInstructions']
        self.assertTrue(isinstance(testInstructions, str), 'Recipe Instructions should be a string')
