import bs4 as bs
import urllib.request
import json


class JsonScrapper():

    def ExtractIngredients(self, jsonDict):

        return jsonDict['recipeIngredient']

    def ExtractInstructions(self, jsonDict):

        if 'recipeInstructions' in jsonDict:

            # Some recipies have their instructions in a list.
            # If this is true, concatinate the text into a single string, and return the single string
            # Else the instructions are already a single string, so simply return it.
            if type(jsonDict['recipeInstructions']) == list:
                instructions = ''
                for item in jsonDict['recipeInstructions']:

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
                return jsonDict['recipeInstructions']

        else:
            return ''

    def ExtractRecipeName(self, jsonDict):
        if 'name' in jsonDict:
            return jsonDict['name']
        elif 'headline' in jsonDict:
            return jsonDict['headline']

    def ExtractRecipeData(self, soup):
        recipeDataJson = soup.find('script', type='application/ld+json')
        jsonDict = json.loads(recipeDataJson.string)
        recipeData = {}
        recipeData['name'] = self.ExtractRecipeName(jsonDict)
        recipeData['recipeIngredient'] = self.ExtractIngredients(jsonDict)
        recipeData['recipeInstructions'] = self.ExtractInstructions(jsonDict)
        return recipeData


class CookingLightScrapper(JsonScrapper):


    def ExtractRecipeData(self, soup):
        """CookingLight uses the JSON format, but there are multiple JSONs in
        each HTML. Pull the second one and use the JSON library to load it."""
        recipeDataJson = soup.find('script', type='application/ld+json')
        rawString = recipeDataJson.string.strip()[1:-1]
        startIndex = rawString.find('},{"@context') + 2
        jsonDict = json.loads(rawString[startIndex:])
        recipeData = {}
        recipeData['name'] = self.ExtractRecipeName(jsonDict)
        recipeData['recipeIngredient'] = self.ExtractIngredients(jsonDict)
        recipeData['recipeInstructions'] = self.ExtractInstructions(jsonDict)
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


class CooksScrapper():

    def ExtractIngredients(self, soup):
        ingredients = []
        for ingredient in soup.find_all('span', class_="ingredient"):
            ingredients.append(ingredient.string)
        return ingredients


    def ExtractInstructions(self, soup):

        instructions = soup.find('div', class_='instructions').get_text()
        return instructions


    def ExtractRecipeName(self, soup):

        # The recipe title is captalized for cooks.com
        # When the title is found, make it all lower case then capitalize the first
        # letter of each word before returning the title.

        for input in soup.find_all('input', attrs={'name':'title'}):
            if 'value' in input.attrs:
                rawName = input['value'].lower()
                name = ''
                for word in rawName.split(' '):
                    name += '{} '.format(word.capitalize())
                return name.strip()


    def ExtractRecipeData(self, soup):
        recipeData = {}
        recipeData['name'] = self.ExtractRecipeName(soup)
        recipeData['recipeIngredient'] = self.ExtractIngredients(soup)
        recipeData['recipeInstructions'] = self.ExtractInstructions(soup)
        return recipeData


class RecipeObjectClass():

    def __init__(self, recipeObj=None):

        if recipeObj is None:
            self.data = {}
            self.validData = False
        else:
            self.data = recipeObj.data
            self.validData = recipeObj.validData


    def GetScrapper(self, url):
        """Gets the class pointer to the specific scrapper based on the URL
        of the food website.

        Different food sites use different methods to format the recipe data
        This function identifies the best scrapper to scrape the recipe data
        and returns it to the calling fucntion

        Args:
            url: The full URL of the food website

        Returns:
            Class pointer for the specific scraper to parse the website
        """

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
        elif 'cooks' in url:
            return CooksScrapper
        else:
            return JsonScrapper


    def GetHtmlData(self, url):
        """Retrieves the HTML data from a url
        Other functions or libraries will be used to parse this data.

        Args:
            url: The website to open and read the HTML data

        Returns:
            If there is an issue opening the website this function will return a blank string
            Otherwise the entire website's HTML data will be returned.
        """

        # Adding a custom header will prevent a 403 Forbidden response from a website
        # Rather than using the default header and retrying on a 403, just send
        # the custom header initially.
        requestHeaders = {}
        requestHeaders['User-Agent'] = 'Chrome Browser'
        source = ''

        # Create a request so headers can be added
        req = urllib.request.Request(url, headers=requestHeaders)
        try:
            with urllib.request.urlopen(req) as response:
                source = response.read()
                print(response.status)
        except urllib.error.HTTPError as httpError:
            print(httpError.code)
            if httpError.code == 403:
                # TODO: Website is still giving 403 Forbidden response.
                # Header might need to be updated.
                pass
        except urllib.error.URLError as urlError:
            # TODO: Investigate what URLErrors could happen
            # and properly handle each one.
            # For now just print the cause so the app doesn't crash
            # on the user.
            print(urlError.reason)

        return source

    def GetRecipeFromUrl(self, url):
        """Determines how to scrape the recipe data using the URL, and passes
        the URL's HTML data to the correct scrapper to extract the recipe data.
        If there is a valid recipe data in the URL the validData flag is set to True
        and use the data from the recipe scrapper
        Otherwise the validData flag is set to false and the data dict is set to empty.

        Args:
            url: The website where the recipe is located.

        Returns:
            None.
        """

        rawHtmlData = self.GetHtmlData(url)

        # If there was an issue getting the HTML data, treat this as invalid data
        # and return.
        if rawHtmlData != '':
            soup = bs.BeautifulSoup(rawHtmlData, 'lxml')
            scrapper = self.GetScrapper(url)
            recipeData = scrapper().ExtractRecipeData(soup)
            if recipeData is not None:
                self.data = recipeData
                self.validData = True
            else:
                self.data = {}
                self.validData = False
                print('Could not find recipe data for {}'.format(url))
                if type(rawHtmlData) is bytes:
                    # TODO: Need to find a way to properly decode these sites.
                    # Beautiful Soup will correctly not find the type, but print
                    # the reason why
                    print('Source is byte string')
        else:
            self.data = {}
            self.validData = False
            print('Raw html data invalid')


    def SetRecipeFromDict(self, recipeDict):
        """This function is used to copy pre-parsed recipe data stored in a dictionary
        format to this object.

        Args:
            recipeDict: A dictionary containing pre-parsed recipe data

        Returns:
            None
        """
        self.data = recipeDict
        self.validData = True


    def GetRecipeName(self):
        """Returns the recipe name to the calling function

        Args:
            None

        Returns:
            If a name wasn't stored, this function will returns a blank string
            Otherwise the name of the recipe is returned.
        """

        if 'name' in self.data:
            return self.data['name']
        else:
            return ''

    def GetIngredients(self):
        """Returns the recipe ingredients to the calling function

        Args:
            None

        Returns:
            If the ingredients weren't stored, this function will returns a blank string
            Otherwise the ingredients of the recipe are returned.
        """

        if 'recipeIngredient' in self.data:
            return self.data['recipeIngredient']
        else:
            return ''


    def GetInstructions(self):
        """Returns the recipe instructions to the calling function

        Args:
            None

        Returns:
            If the instructions weren't stored, this function will returns a blank string
            Otherwise the instructions of the recipe are returned.
        """

        if 'recipeInstructions' in self.data:
            return self.data['recipeInstructions']
        else:
            return 'a'


    def GetRecipeErrors(self):
        """This function looks at all of the parts of the recipe and looks for issues.
        If there are any issues the user should be notified.

        Args:
            None

        Returns:
            A string with all of the errors that were found.
            If there are no errors, a blank string is returned
        """

        errorStr = ''

        if self.GetRecipeName() == '':
            errorStr += 'Problem finding Recipe Name\n'
        if self.GetIngredients() == '':
            errorStr += 'Problem finding Recipe Ingredients\n'
        if self.GetInstructions() == '':
            errorStr += 'Problem finding Recipe Instructions\n'

        return errorStr


    def GetData(self):
        """Returns the dictionary data of the recipie to the calling function

        Args:
            None

        Returns:
            The dictionary data.
        """

        return self.data
