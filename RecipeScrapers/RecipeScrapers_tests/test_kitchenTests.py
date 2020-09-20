import unittest
import bs4 as bs
import os
from RecipeScrapers import TheKitchnScraper


class KitchenScrapperTestClass(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        self.recipeData = ''

    def read_recipe_data(self):
        """
            Helper function to read the actual recipe from a test HTML file
            This function will open the file, creat a soup object from it
            and call the recipe scraper to extract the data.
        """

        with open(os.path.join(os.path.dirname(__file__),'testHtml/thekitchnTest1.html'),'r') as inHtml:
            soup = bs.BeautifulSoup(inHtml.read(), 'lxml')
            self.recipeData = TheKitchnScraper().extract_recipe_data(soup)

    def read_empty_recipe_data(self):
        """
            Helper function to parse an empty HTML string
            This will be used to test the case where recipe data
            is not found.
        """

        soup = bs.BeautifulSoup("<html></html>", 'lxml')
        self.recipeData = TheKitchnScraper().extract_recipe_data(soup)

    def test_recipe_name_get_correct_name(self):

        self.read_recipe_data()
        actual_name = 'How To Make the Easiest Pasta Salad'
        test_name = self.recipeData['name']
        self.assertEqual(actual_name, test_name, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actual_name, test_name))

    def test_recipe_name_name_not_found(self):

        actual_name = ''
        self.read_empty_recipe_data()
        test_name = self.recipeData['name']
        self.assertEqual(actual_name, test_name, 'Recipe name mismath.\nExpected {}\nGot {}'.format(actual_name, test_name))

    def test_recipe_ingredients_gets_correct_ingredients(self):

        self.read_recipe_data()
        actualIngredients = ['1/2 cup olive oil',
                             '1/4 cup red wine vinegar',
                             '2 teaspoons dried Italian seasoning',
                             '1/2 teaspoon granulated sugar',
                             '1 clove garlic, minced',
                             '1/2 teaspoon kosher salt',
                             '1/4 teaspoon freshly ground black pepper',
                             '1/2 medium red onion, finely chopped',
                             '8 ounces dried short pasta, such as rotini',
                             '8 ounces cherry tomatoes, halved or quartered',
                             '1 small English cucumber, quartered lengthwise, then thinly sliced crosswise',
                             '4 ounces mini mozzarella balls, drained and halved',
                             '4 ounces salami slices, cut into 1/2-inch-wide strips',
                             '1/2 cup pitted kalamata olives, halved',
                             '1/4 cup coarsely chopped fresh parsley leaves']
        actual_ingredients_str = ''
        for recipe_instruction_item in actualIngredients:
            actual_ingredients_str += '{}\n'.format(recipe_instruction_item.strip())
        test_ingredients = self.recipeData['recipeIngredient']
        self.assertTrue(isinstance(test_ingredients, str), 'Ingredients should be a list')
        self.assertEqual(actual_ingredients_str, test_ingredients, 'Recipe Ingredient Mismatch')

    def test_recipe_ingredients_ingredients_not_found(self):

        self.read_empty_recipe_data()
        actual_ingredients_str = ''
        test_ingredients = self.recipeData['recipeIngredient']
        self.assertTrue(isinstance(test_ingredients, str), 'Ingredients should be a string')
        self.assertEqual(actual_ingredients_str, test_ingredients, 'Recipe Ingredient Mismatch')

    def test_recipe_instructions(self):

        self.read_recipe_data()
        testInstructions = self.recipeData['recipeInstructions']
        self.assertTrue(isinstance(testInstructions, str), 'Recipe Instructions should be a string')
