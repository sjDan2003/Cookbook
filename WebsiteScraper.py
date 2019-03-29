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

        req = urllib.request.Request(url)
        retry = True
        while retry is True:
            try:
                response = urllib.request.urlopen(req)
            except urllib.error.HTTPError as e:
                print(e.code)
                #print(e.read())
                if e.code == 403:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Magic Browser'})
                else:
                    retry = False
            else:
                source = response.read()
                soup = bs.BeautifulSoup(source, 'lxml')

                self.data = json.loads(soup.find('script', type='application/ld+json').text)
                self.validData = True
                print(response.status)

                response.close()
                retry = False

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

            # Some recipies have their instructions in a list.
            # If this is true, concatinate the text into a single string, and return the single string
            # Else the instructions are already a single string, so simply return it.
            if type(self.data['recipeInstructions']) == list:
                instructions = ''
                for item in self.data['recipeInstructions']:
                    instructions += '{} \n'.format(item['text'])
                return instructions
            else:
                return self.data['recipeInstructions']

        else:
            return ''
