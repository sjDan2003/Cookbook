import unittest
import bs4 as bs
import os
from WebsiteScraper import TheKitchnScrapper


class KitchenScrapperTestClass(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        with open(os.path.join(os.path.dirname(__file__),'testHtml/thekitchnTest1.html'),'r') as inHtml:
            soup = bs.BeautifulSoup(inHtml.read(), 'lxml')
            self.recipeData = TheKitchnScrapper().ExtractRecipeData(soup)

    def test_RecipeName(self):

        actualName = 'Carrot Soup'
        testName = self.recipeData['name']
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))

    def test_RecipeIngredients(self):

        actualIngredients = ['2 tablespoons olive or coconut oil',
                             '1 small yellow onion, chopped',
                             '2 tablespoons red curry paste',
                             '1 (1-inch) piece fresh ginger, peeled and thinly sliced (about 2 tablespoons)',
                             '1 pound carrots (about 8 medium), peeled and coarsely chopped',
                             '1 (14 to 15-ounce) can light coconut milk',
                             '1 1/2 cups low-sodium vegetable broth',
                             '1/4 cup creamy natural peanut or almond butter (such as Trader Joe’s Creamy Unsalted Almond Butter)',
                             'Kosher salt',
                             'Freshly ground black pepper',
                             'For serving: chopped fresh cilantro leaves and tender stems, chopped roasted peanuts, and lime wedges']
        testIngredients = self.recipeData['recipeIngredient']
        self.assertTrue(isinstance(testIngredients, list), 'Ingredients should be a list')
        self.assertEqual(actualIngredients, testIngredients, 'Recipe Ingredient Mismatch')

    def test_RecipeInstructions(self):

        testInstructions = self.recipeData['recipeInstructions']
        self.assertTrue(isinstance(testInstructions, str), 'Recipe Instructions should be a string')
