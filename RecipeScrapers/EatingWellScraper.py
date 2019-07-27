import bs4 as bs

class EatingWellScraper():

    def ExtractIngredients(self, soup):
        ingredients = []
        for ingredient in soup.find_all('span', itemprop='ingredients'):
            ingredients.append(ingredient.string.strip())
        return ingredients

    def ExtractInstructions(self, soup):

        instructions = ''
        for instuction in soup.find_all('span', class_="recipeDirectionsListItem"):
            # Eating well has an extra recipe direction that has no text and doesn't
            # pertain to the instructions.
            # If this attribute is found ignore it.
            if 'ng-bind-html' not in instuction.attrs:
                instructions += '{}\n'.format(instuction.string.strip())
        return instructions

    def ExtractRecipeName(self, soup):

        return soup.find('meta', property='og:title')['content']

    def ExtractRecipeData(self, soup):
        recipeData = {}
        recipeData['name'] = self.ExtractRecipeName(soup)
        recipeData['recipeIngredient'] = self.ExtractIngredients(soup)
        recipeData['recipeInstructions'] = self.ExtractInstructions(soup)
        return recipeData