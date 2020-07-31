import unittest
import bs4 as bs
import os
from .TestHelpers import read_recipe_data, read_empty_recipe_data
from RecipeScrapers import AllRecipesScraper


class AllRecipesScrapperTestClass(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        self.recipeData = ''

    def read_recipe_data(self):
        """
            Helper function to read the actual recipe from a test HTML file
            This function will open the file, creat a soup object from it
            and call the recipe scraper to extract the data.
        """

        with open(os.path.join(os.path.dirname(__file__),'testHtml/allrecipesTest1.html'),'r') as inHtml:
            soup = bs.BeautifulSoup(inHtml.read(), 'lxml')
            self.recipeData = AllRecipesScraper().extract_recipe_data(soup)

    def read_empty_recipe_data(self):
        """
            Helper function to parse an empty HTML string
            This will be used to test the case where recipe data
            is not found.
        """

        soup = bs.BeautifulSoup("<html></html>", 'lxml')
        self.recipeData = AllRecipesScraper().extract_recipe_data(soup)

    def test_recipe_name_get_correct_name(self):

        self.read_recipe_data()
        actualName = 'Janet\'s Rich Banana Bread'
        testName = self.recipeData['name']
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))

    def test_recipe_name_name_not_found(self):

        actualName = ''
        self.read_empty_recipe_data()
        testName = self.recipeData['name']
        self.assertEqual(actualName, testName, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actualName, testName))

    def test_recipe_ingredients_gets_correct_ingredients(self):

        self.read_recipe_data()
        actualIngredients = ["½ cup butter, melted",
                             "1 cup white sugar",
                             "2   eggs",
                             "1 teaspoon vanilla extract",
                             "1 ½ cups all-purpose flour",
                             "1 teaspoon baking soda",
                             "½ teaspoon salt",
                             "½ cup sour cream",
                             "½ cup chopped walnuts",
                             "2   medium bananas, sliced"
                            ]
        actualIngredientsStr = ''
        for recipe_instruction_item in actualIngredients:
            actualIngredientsStr += '{}\n'.format(recipe_instruction_item.strip())
        testIngredients = self.recipeData['recipeIngredient']
        self.assertTrue(isinstance(testIngredients, str), 'Ingredients should be a string')
        self.assertEqual(actualIngredientsStr, testIngredients, 'Recipe Ingredient Mismatch')

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