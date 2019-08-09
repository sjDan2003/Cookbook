import bs4 as bs

class TheKitchnScraper():

    def Extractrecipe_name(self, soup):

        return soup.find('h2', class_='Recipe__title').string

    def ExtractIngredients(self, soup):

        ingredients = []
        ingredient = ''

        # Find all of the ingredients and add them to the ingredient list
        # Ingredient quantiy and text are seperated by span tags, so this
        # function will have to combine all of the text between span tags.
        for ingredientClass in soup.find_all('li', class_='Recipe__ingredient'):
            for ingredientItem in ingredientClass.find_all('span'):
                ingredient += ingredientItem.get_text()
            ingredients.append(ingredient.strip())
            ingredient = ''

        return ingredients

    def ExtractInstructions(self, soup):
        instructions = ''

        for instruction in soup.find_all('li', class_='Recipe__instruction-step'):
            instructions += '{}\n'.format(instruction.string)

        return instructions

    def ExtractRecipeData(self, soup):
        recipeData = {}
        recipeSoup = soup.find('div', class_='Recipe')
        recipeData['name'] = self.Extractrecipe_name(recipeSoup)
        recipeData['recipeIngredient'] = self.ExtractIngredients(recipeSoup)
        recipeData['recipeInstructions'] = self.ExtractInstructions(recipeSoup)
        return recipeData