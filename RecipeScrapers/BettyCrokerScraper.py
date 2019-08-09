import bs4 as bs

class BettyCrockerScraper():

    def ExtractIngredients(self, soup):
        ingredients = []
        for ingredient in soup.find_all('div', class_='recipePartIngredient'):
            quantiy = ingredient.find('div', class_='quantity').get_text().strip()
            description = ingredient.find('div', class_='description').get_text().strip()
            ingredients.append('{} {}'.format(quantiy, description))
        return ingredients

    def ExtractInstructions(self, soup):

        instructions = ''
        for instuction in soup.find_all('div', class_="recipePartStepDescription"):
            instructions += '{}\n'.format(instuction.string.strip())
        return instructions

    def Extractrecipe_name(self, soup):

        return soup.find('h1', class_="recipePartTitleText").string

    def ExtractRecipeData(self, soup):
        recipeData = {}
        recipeData['name'] = self.Extractrecipe_name(soup)
        recipeData['recipeIngredient'] = self.ExtractIngredients(soup)
        recipeData['recipeInstructions'] = self.ExtractInstructions(soup)
        return recipeData