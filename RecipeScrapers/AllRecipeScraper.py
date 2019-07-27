import bs4 as bs

class AllRecipesScraper():

    def ExtractIngredients(self, soup):
        ingredients = []
        for ingredient in soup.find_all('span', itemprop="recipeIngredient"):
            ingredients.append(ingredient.string)
        return ingredients

    def ExtractInstructions(self, soup):

        instructions = ''
        for instuction in soup.find_all('span', class_="recipe-directions__list--item"):
            instructions += '{}\n'.format(instuction.string)
        return instructions

    def ExtractRecipeName(self, soup):

        return soup.find('h1', id="recipe-main-content").string

    def ExtractRecipeData(self, soup):
        recipeData = {}
        recipeData['name'] = self.ExtractRecipeName(soup)
        recipeData['recipeIngredient'] = self.ExtractIngredients(soup)
        recipeData['recipeInstructions'] = self.ExtractInstructions(soup)
        return recipeData