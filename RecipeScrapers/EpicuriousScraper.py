import bs4 as bs
import json


class EpicuriousScraper():

    def Extractrecipe_name(self, soup):
        """One of the places where the recipe name is stored on epicurious is
        in a variable called digital data. This variable stores a dictionary objectn
        containing not only the recipe name, but other information that could be
        useful in the future.
        """
        recipe_name = ''
        for item in soup.find_all('script', type='text/javascript'):
            searchStr = 'var digitalData = '
            if searchStr in item.string:

                # Removing leading and trailing whitespace around the item
                itemString = item.string.strip()

                # Strip the variable name out of the string
                digitalDataVar = itemString[len(searchStr):(len(itemString) - 1)]

                # Convert the string to a dict
                jsonDigitalData = json.loads(digitalDataVar)
                recipe_name = jsonDigitalData['display']
                break

        return recipe_name

    def ExtractIngredients(self, soup):

        ingredients = []

        for ingredient in soup.find_all('li', class_='ingredient'):
            ingredients.append(ingredient.string)

        return ingredients

    def ExtractInstructions(self, soup):

        instructions = ''

        for instruction in soup.find_all('li', class_='preparation-step'):
            instructions += '{}\n'.format(instruction.string.strip())

        return instructions

    def ExtractRecipeData(self, soup):
        recipeData = {}
        recipeData['name'] = self.Extractrecipe_name(soup)
        recipeData['recipeIngredient'] = self.ExtractIngredients(soup)
        recipeData['recipeInstructions'] = self.ExtractInstructions(soup)
        return recipeData