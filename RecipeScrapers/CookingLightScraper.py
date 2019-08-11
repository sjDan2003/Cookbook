import json
from .JsonScraper import JsonScraper

class CookingLightScraper(JsonScraper):
    """This class is responsible for extracting recipe data
    from cookinglight.com
    """

    def extract_recipe_data(self, soup):
        """CookingLight uses the JSON format, but there are multiple JSONs in
        each HTML. Pull the second one and use the JSON library to load it.

        Args:
            soup: Beautiful Soup object containing the recipe data

        Returns:
            A dictionary containing all of the relevant recipe data
        """

        recipe_data_json = soup.find('script', type='application/ld+json')
        raw_string = recipe_data_json.string.strip()[1:-1]
        start_index = raw_string.find('},{"@context') + 2
        json_dict = json.loads(raw_string[start_index:])
        recipe_data = {}
        recipe_data['name'] = self.extract_recipe_name(json_dict)
        recipe_data['recipeIngredient'] = self.extract_ingredients(json_dict)
        recipe_data['recipeInstructions'] = self.extract_instructions(json_dict)
        return recipe_data
