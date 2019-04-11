import bs4 as bs
import urllib.request
import json


class JsonScrapper():


    def ExtractRecipeData(self, soup):
        recipeDataJson = soup.find('script', type='application/ld+json')
        print(recipeDataJson.string)
        recipeData = json.loads(recipeDataJson.string)
        return recipeData


class CookingLightScrapper():


    def ExtractRecipeData(self, soup):
        """CookingLight uses the JSON format, but there are multiple JSONs in
        each HTML. Pull the second one and use the JSON library to load it."""
        recipeDataJson = soup.find('script', type='application/ld+json')
        rawString = recipeDataJson.string.strip()[1:-1]
        startIndex = rawString.find('},{"@context') + 2
        recipeData = json.loads(rawString[startIndex:])

        return recipeData


class AllRecipesScrapper():


    def ExtractIngredients(self, soup):
        ingredients = []
        for ingredient in soup.find_all('span', itemprop="recipeIngredient"):
            print(ingredient.string)
            ingredients.append(ingredient.string)
        return ingredients


    def ExtractInstructions(self, soup):

        instructions = ''
        for instuction in soup.find_all('span', class_="recipe-directions__list--item"):
            print(instuction.string)
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


class EpicuriousScrapper():

    def ExtractRecipeName(self, soup):
        """One of the places where the recipe name is stored on epicurious is
        in a variable called digital data. This variable stores a dictionary objectn
        containing not only the recipe name, but other information that could be
        useful in the future.
        """
        recipeName = ''
        for item in soup.find_all('script', type='text/javascript'):
            searchStr = 'var digitalData = '
            if searchStr in item.string:

                # Removing leading and trailing whitespace around the item
                itemString = item.string.strip()

                # Strip the variable name out of the string
                digitalDataVar = itemString[len(searchStr) : len(itemString) - 1]

                #Convert the string to a dict
                jsonDigitalData = json.loads(digitalDataVar)
                recipeName = jsonDigitalData['display']
                break

        return recipeName


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
        recipeData['name'] = self.ExtractRecipeName(soup)
        recipeData['recipeIngredient'] = self.ExtractIngredients(soup)
        recipeData['recipeInstructions'] = self.ExtractInstructions(soup)
        return recipeData


class TheKitchnScrapper():

    def ExtractRecipeName(self, soup):

        return soup.find('h2', class_='Recipe__title').string

    def ExtractIngredients(self, soup):

        ingredients = []
        ingredient  = ''

        # Find all of the ingredients and add them to the ingredient list
        # Ingredient quantiy and text are seperated by span tags, so this function will have to
        # combine all of the text between span tags.
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
        recipeData['name'] = self.ExtractRecipeName(recipeSoup)
        recipeData['recipeIngredient'] = self.ExtractIngredients(recipeSoup)
        recipeData['recipeInstructions'] = self.ExtractInstructions(recipeSoup)
        return recipeData


class BettyCrockerScrapper():

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


    def ExtractRecipeName(self, soup):

        return soup.find('h1', class_="recipePartTitleText").string


    def ExtractRecipeData(self, soup):
        recipeData = {}
        recipeData['name'] = self.ExtractRecipeName(soup)
        recipeData['recipeIngredient'] = self.ExtractIngredients(soup)
        recipeData['recipeInstructions'] = self.ExtractInstructions(soup)
        return recipeData


class EatingWellScrapper():

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


class RecipeObjectClass:

    def __init__(self, recipeObj=None):

        if recipeObj is None:
            self.data = {}
            self.validDatSa = False
        else:
            self.data = recipeObj.data
            self.validData = recipeObj.validData


    def GetScrapper(self, url):

        """Different food sites use different methods to format the recipe data
        This function identifies the best scrapper to scrape the recipe data
        and returns it to the calling fucntion"""

        if 'allrecipes' in url:
            return AllRecipesScrapper
        elif 'epicurious' in url:
            return EpicuriousScrapper
        elif 'cookinglight' in url or 'myrecipes' in url:
            return CookingLightScrapper
        elif 'thekitchn' in url:
            return TheKitchnScrapper
        elif 'bettycrocker' in url:
            return BettyCrockerScrapper
        elif 'eatingwell' in url:
            return EatingWellScrapper
        else:
            return JsonScrapper

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
                scrapper = self.GetScrapper(url)
                recipeData = scrapper().ExtractRecipeData(soup)
                if recipeData is not None:
                    self.data = recipeData
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
