import bs4 as bs
import urllib.request
import json


class RecipeObjectClass:

    def __init__(self, recipeObj=None):

        if recipeObj is None:
            self.data = {}
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
                recipeData = soup.find('script', type='application/ld+json')
                if recipeData is not None:
                    self.data = json.loads(recipeData.text)
                    self.validData = True
                else:
                    self.data = {}
                    self.validData = False
                    print('Could not find recipe data for {}'.format(url))
                    if type(source) is bytes:
                        # TODO: Need to find a way to properly decode these sites.
                        # Beautiful Soup will correctly not find the type, but print
                        # the reason why
                        print('Source is byte string')
                print(response.status)

                response.close()
                retry = False

    def GetRecipeFromDict(self, recipeDict):
        """If the recipe is already in dictionary format, then simply copy its data
        to this object and set this object's value to true"""
        self.data = recipeDict
        self.validData = True


    def GetRecipeName(self):

        if 'name' in self.data:
            return self.data['name']
        elif 'headline' in self.data:
            return self.data['headline']
        else:
            print('Could not find name')
            return ''

    def GetIngredients(self):

        if 'recipeIngredient' in self.data:
            return self.data['recipeIngredient']
        else:
            return ''


    def GetInstructions(self):

        if 'recipeInstructions' in self.data:

            # Some recipies have their instructions in a list.
            # If this is true, concatinate the text into a single string, and return the single string
            # Else the instructions are already a single string, so simply return it.
            if type(self.data['recipeInstructions']) == list:
                instructions = ''
                for item in self.data['recipeInstructions']:

                    # Some websites use a itemListElement for their ingredients.
                    if 'itemListElement' in item:
                        itemList = item['itemListElement']
                        for item in itemList:
                            instructions += '{} \n'.format(item['text'].strip())
                    else:
                        try:
                            instructions += '{} \n'.format(item['text'].strip())
                        except TypeError:
                            instructions += '{} \n'.format(item.strip())
                return instructions
            else:
                return self.data['recipeInstructions']

        else:
            return ''


    def GetRecipeErrors(self):

        errorStr = ''

        if self.GetRecipeName() == '':
            errorStr += 'Problem finding Recipe Name\n'
        if self.GetIngredients() == '':
            errorStr += 'Problem finding Recipe Ingredients\n'
        if self.GetInstructions() == '':
            errorStr += 'Problem finding Recipe Instructions\n'

        return errorStr

    def GetData(self):

        return self.data
