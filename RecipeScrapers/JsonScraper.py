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
            for ingredient in json_dict['recipeIngredient']:
                ingredients += '{}\n'.format(ingredient)

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
                            instructions += '{} \n'.format(instruction_list['text'].strip())
                        except TypeError:
                            instructions += '{} \n'.format(instruction_list.strip())
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

    @staticmethod
    def extract_recipe_image_url(recipe_dict):
        """Extracts the recipe's image URL from the recipe dictionary
        This URL will be used to download the image by the main recipe object

        Args:
            recipe_dict: Dictionary object containing the entire recipe

        Returns:
            A string with the recipe's image url if the image tag exists
            An empty string if the name can not be found
        """

        image_url = ''

        if 'image' in recipe_dict:

            image_data = recipe_dict['image']

            if 'url' in image_data:
                image_url = image_data['url']
            elif isinstance(image_data, list):
                image_url = image_data[-1]
            else:
                print("Unknown Json image data format")

        return image_url

    def extract_recipe_data(self, soup):
        """Manages the collection of all recipe data and returns that
        data back to the calling function.

        Args:
            soup: Beautiful Soup object containing the recipe data

        Returns:
            A dictionary containing all of the relevant recipe data
        """

        recipe_data = {}
        recipe_data['name'] = ''
        recipe_data['recipeInstructions'] = ''
        recipe_data['recipeIngredient'] = ''
        recipe_data['image'] = ''

        # Find all scripts that would contain recipe data
        # Some sites have only one, while others have data spead over multiple scripts
        recipe_data_json_list = soup.find_all('script', type='application/ld+json')

        if recipe_data_json_list != None:

            # Loop over all lists, picking data from each one
            for recipe_data_json in recipe_data_json_list:

                json_dict = json.loads(recipe_data_json.string)
                if isinstance(json_dict, list):
                    json_dict = json_dict[0]

                # TODO: Need to detect if two scripts have the same tags but different information
                recipe_data['name'] = self.extract_recipe_name(json_dict)
                recipe_data['recipeIngredient'] = self.extract_ingredients(json_dict)
                recipe_data['recipeInstructions'] = self.extract_instructions(json_dict)
                recipe_data['image'] = self.extract_recipe_image_url(json_dict)

        return recipe_data
