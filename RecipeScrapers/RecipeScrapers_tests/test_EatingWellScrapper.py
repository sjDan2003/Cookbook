import unittest
import bs4 as bs
import os
from RecipeScrapers import EatingWellScraper


class KitchenScrapperTestClass(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        with open(os.path.join(os.path.dirname(__file__),'testHtml/eatingWellTest1.html'),'r') as inHtml:
            soup = bs.BeautifulSoup(inHtml.read(), 'lxml')
            self.recipeData = EatingWellScraper().ExtractRecipeData(soup)

    def test_recipe_name(self):

        actualName = 'Gluten-Free Pumpkin Waffles Recipe'
        testName = self.recipeData['name']
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))

    def test_recipe_ingredients(self):

        actualIngredients = ['Nonstick cooking spray',
                             '½ cup gluten-free all-purpose flour',
                             '½ cup vanilla-flavor whey protein powder',
                             '¼ cup coconut flour', '¼ cup flaxseed meal',
                             '¼ cup sugar (see Tips)',
                             '2 teaspoons arrowroot or cornstarch',
                             '2 teaspoons baking powder',
                             '2 teaspoons ground cinnamon',
                             '½ teaspoon baking soda',
                             '½ teaspoon ground ginger',
                             '1 cup unsweetened almond milk',
                             '¾ cup canned pumpkin puree (see Tips)',
                             '3 egg whites', '1 tablespoon grapeseed oil',
                             '1 teaspoon vanilla', 'Sugar-free maple syrup (optional)',
                             'Frozen light whipped dessert topping, thawed (optional)',
                             'Ground cinnamon (optional)']
        testIngredients = self.recipeData['recipeIngredient']
        self.assertTrue(isinstance(testIngredients, list), 'Ingredients should be a list')
        self.assertEqual(actualIngredients, testIngredients, 'Recipe Ingredient Mismatch')

    def test_recipe_instructions(self):

        testInstructions = self.recipeData['recipeInstructions']
        self.assertTrue(isinstance(testInstructions, str), 'Recipe Instructions should be a string')
