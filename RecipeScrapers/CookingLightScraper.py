import json
import bs4 as bs
from .JsonScraper import JsonScraper


class CookingLightScraper(JsonScraper):

    def ExtractRecipeData(self, soup):
        """CookingLight uses the JSON format, but there are multiple JSONs in
        each HTML. Pull the second one and use the JSON library to load it."""
        recipeDataJson = soup.find('script', type='application/ld+json')
        rawString = recipeDataJson.string.strip()[1:-1]
        startIndex = rawString.find('},{"@context') + 2
        jsonDict = json.loads(rawString[startIndex:])
        recipeData = {}
        recipeData['name'] = self.Extractrecipe_name(jsonDict)
        recipeData['recipeIngredient'] = self.ExtractIngredients(jsonDict)
        recipeData['recipeInstructions'] = self.ExtractInstructions(jsonDict)
        return recipeData