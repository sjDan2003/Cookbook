import json

class JsonScraper():
    """This class extracts recipe information from a website that uses
    the standard JSON format in the HTML data.

    Attributes:
        None
    """

    @staticmethod
    def extract_ingredients(json_dict):
        """Extracts the ingredients from the soup object

        Args:
            json_dict: Dictionary object containing the recipe information

        Returns:
            The list of ingredients
        """

        ingredients = ''

        if 'recipeIngredient' in json_dict:
            ingredients = json_dict['recipeIngredient']

        return ingredients

    @staticmethod
    def extract_instructions(json_dict):
        """Extracts the recipe instructions from the soup object

        Args:
            json_dict: Dictionary object containing the recipe information

        Returns:
            A string with the recipe instructions
        """

        instructions = ''

        if 'recipeInstructions' in json_dict:

            # Some recipies have their instructions in a list.
            # If this is true, concatinate the text into a single string
            # and return the single string
            # Else the instructions are already a single string
            # so simply return it.
            if isinstance(json_dict['recipeInstructions'], list):

                for instruction_list in json_dict['recipeInstructions']:

                    # Some websites use a itemListElement for their
                    # ingredients.
                    if 'itemListElement' in instruction_list:
                        item_list = item['itemListElement']
                        for item in item_list:
                            instructions += '{} \n'.format(item['text'].strip())
                    else:
                        try:
                            instructions += '{} \n'.format(item['text'].strip())
                        except TypeError:
                            instructions += '{} \n'.format(item.strip())
                return instructions
            else:
                instructions = json_dict['recipeInstructions']

        return instructions

    @staticmethod
    def extract_recipe_name(json_dict):
        """Extracts the recipe's name from the soup object

        Args:
            json_dict: Dictionary object containing the recipe information

        Returns:
            A string with the recipe's name
        """

        recipe_name = ''

        if 'name' in json_dict:
            recipe_name = json_dict['name']
        elif 'headline' in json_dict:
            recipe_name = json_dict['headline']

        return recipe_name

    def extract_recipe_data(self, soup):
        """Manages the collection of all recipe data and returns that
        data back to the calling function.

        Args:
            soup: Beautiful Soup object containing the recipe data

        Returns:
            A dictionary containing all of the relevant recipe data
        """

        recipe_data_json = soup.find('script', type='application/ld+json')
        json_dict = json.loads(recipe_data_json.string)
        if isinstance(json_dict, list):
            json_dict = json_dict[0]
        recipe_data = {}
        recipe_data['name'] = self.extract_recipe_name(json_dict)
        recipe_data['recipeIngredient'] = self.extract_ingredients(json_dict)
        recipe_data['recipeInstructions'] = self.extract_instructions(json_dict)
        return recipe_data
