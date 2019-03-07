import bs4 as bs
import urllib.request
import json


class RecipeObjectClass:

    def __init__(self, url):

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

        return self.data['headline']

    def GetIngredients(self):

        return self.data['recipeIngredient']

    def GetInstructions(self):

        return self.data['recipeInstructions']
