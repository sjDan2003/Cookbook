import unittest
import bs4 as bs
import os
from RecipeScrapers import CooksScraper


class CooksScrapperTestClass(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        with open(os.path.join(os.path.dirname(__file__),'testHtml/cooksTest1.html'),'r') as inHtml:
            soup = bs.BeautifulSoup(inHtml.read(), 'lxml')
            self.recipeData = CooksScraper().extract_recipe_data(soup)

    def test_recipe_name(self):

        actual_name = 'Genuine Virginia Baked Ham'
        test_name = self.recipeData['name']
        self.assertEqual(actual_name, test_name, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actual_name, test_name))

    def test_recipe_ingredients(self):

        actual_ingredients = ['1 small, rather lean ham',
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
        test_ingredients = self.recipeData['recipeIngredient']
        self.assertTrue(isinstance(test_ingredients, list), 'Ingredients should be a list')
        self.assertEqual(actual_ingredients, test_ingredients, 'Recipe Ingredient Mismatch')

    def test_recipe_instructions(self):

        test_instructions = self.recipeData['recipeInstructions']
        self.assertTrue(isinstance(test_instructions, str), 'Recipe Instructions should be a string')
