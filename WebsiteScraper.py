import bs4 as bs
import urllib.request
import json


class RecipeObjectClass:

    def __init__(self, recipeObj=None):

        if recipeObj is None:
            self.data = ''
            self.validData = False
        else:
            self.data = recipeObj.data
            self.validData = recipeObj.validData

    def GetRecipeFromUrl(self, url):

        with urllib.request.urlopen(url) as response:

            if response.status == 200:
                source = response.read()
                soup = bs.BeautifulSoup(source, 'lxml')

                self.data = json.loads(soup.find('script', type='application/ld+json').text)
                self.validData = True
                print(response.status)
            else:
                self.validData = False

    def GetRecipeName(self):

        if 'name' in self.data:
            return self.data['name']
        elif 'headline' in self.data:
            return self.data['headline']
        else:
            return ''

    def GetIngredients(self):

        return self.data['recipeIngredient']

    def GetInstructions(self):

        if 'recipeInstructions' in self.data:

            return self.data['recipeInstructions']

        else:

            return ''
