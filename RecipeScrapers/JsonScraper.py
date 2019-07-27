import json


class JsonScraper():

    def ExtractIngredients(self, jsonDict):

        if 'recipeIngredient' in jsonDict:
            return jsonDict['recipeIngredient']
        else:
            return ''

    def ExtractInstructions(self, jsonDict):

        if 'recipeInstructions' in jsonDict:

            # Some recipies have their instructions in a list.
            # If this is true, concatinate the text into a single string
            # and return the single string
            # Else the instructions are already a single string
            # so simply return it.
            if type(jsonDict['recipeInstructions']) == list:
                instructions = ''
                for item in jsonDict['recipeInstructions']:

                    # Some websites use a itemListElement for their
                    # ingredients.
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
        else:
            return ''

    def ExtractRecipeData(self, soup):
        recipeDataJson = soup.find('script', type='application/ld+json')
        jsonDict = json.loads(recipeDataJson.string)
        if type(jsonDict) == list:
            jsonDict = jsonDict[0]
        recipeData = {}
        recipeData['name'] = self.ExtractRecipeName(jsonDict)
        recipeData['recipeIngredient'] = self.ExtractIngredients(jsonDict)
        recipeData['recipeInstructions'] = self.ExtractInstructions(jsonDict)
        return recipeData