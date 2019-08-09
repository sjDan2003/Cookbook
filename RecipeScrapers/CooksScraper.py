import bs4 as bs

class CooksScraper():

    def ExtractIngredients(self, soup):
        ingredients = []
        for ingredient in soup.find_all('span', class_="ingredient"):
            ingredients.append(ingredient.string)
        return ingredients

    def ExtractInstructions(self, soup):

        instructions = soup.find('div', class_='instructions').get_text()
        return instructions

    def Extractrecipe_name(self, soup):

        # The recipe title is captalized for cooks.com
        # When the title is found, make it all lower case then capitalize
        # the first letter of each word before returning the title.

        for input in soup.find_all('input', attrs={'name': 'title'}):
            if 'value' in input.attrs:
                rawName = input['value'].lower()
                name = ''
                for word in rawName.split(' '):
                    name += '{} '.format(word.capitalize())
                return name.strip()

    def ExtractRecipeData(self, soup):
        recipeData = {}
        recipeData['name'] = self.Extractrecipe_name(soup)
        recipeData['recipeIngredient'] = self.ExtractIngredients(soup)
        recipeData['recipeInstructions'] = self.ExtractInstructions(soup)
        return recipeData