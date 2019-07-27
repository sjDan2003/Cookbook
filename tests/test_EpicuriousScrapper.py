import unittest
import bs4 as bs
import os
from RecipeScrapers import EpicuriousScraper


class EpicuriousScrapperTestClass(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        with open(os.path.join(os.path.dirname(__file__),'testHtml/epicuriousTest1.html'),'r') as inHtml:
            self.soup = bs.BeautifulSoup(inHtml.read(), 'lxml')

    def test_RecipeName(self):
        actualName = 'Slow-Roasted Chicken with Honey-Glazed Carrots and Ginger'
        testName = EpicuriousScraper().ExtractRecipeName(self.soup)
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))

    def test_RecipeIngredients(self):

        actualIngredients = ['1 (3 1/2–4-lb.) chicken',
                             'Kosher salt',
                             '1 head of garlic, halved crosswise, plus 4 cloves, thinly sliced',
                             '1 1/2 lb. carrots, scrubbed, cut in half',
                             '8 small shallots, peeled',
                             '1 (2") piece ginger, unpeeled, thinly sliced',
                             '2 Tbsp. unsalted butter', '1 Tbsp. honey',
                             '2 Tbsp. extra-virgin olive oil',
                             '1 tsp. crushed red pepper flakes',
                             '1/4 cup fresh lime juice']
        testIngredients = EpicuriousScraper().ExtractIngredients(self.soup)
        self.assertTrue(isinstance(testIngredients, list), 'Ingredients should be a list')
        self.assertEqual(actualIngredients, testIngredients, 'Recipe Ingredient Mismatch')

    def test_RecipeInstructions(self):

        testInstructions = EpicuriousScraper().ExtractInstructions(self.soup)
        self.assertTrue(isinstance(testInstructions, str), 'Recipe Instructions should be a string')
