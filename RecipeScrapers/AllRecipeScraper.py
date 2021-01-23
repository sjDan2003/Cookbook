import json

class AllRecipesScraper():
    """This class is responsible for extracting recipe data
    from allrecipes.com
    """

    @staticmethod
    def extract_ingredients(recipe_dict):
        """Extracts the ingredients from the recipe dictionary

        Args:
            recipe_dict: Dictionary object containing the entire recipe

        Returns:
            A string with the recipe ingredients
        """

        ingredients = ''

        if 'recipeIngredient' in recipe_dict:
            for ingredient in recipe_dict['recipeIngredient']:
                ingredients += '{}\n'.format(ingredient.strip())

        return ingredients

    @staticmethod
    def extract_instructions(recipe_dict):
        """Extracts the recipe instructions from the recipe dictionary

        Args:
            recipe_dict: Dictionary object containing the entire recipe

        Returns:
            A string with the recipe instructions
        """

        instructions = ''

        if 'recipeInstructions' in recipe_dict:
            recipe_instruction_list = recipe_dict['recipeInstructions']
            for recipe_instruction_item in recipe_instruction_list:
                instructions += '{}\n'.format(recipe_instruction_item['text'].strip())

        return instructions


    @staticmethod
    def extract_recipe_name(recipe_dict):
        """Extracts the recipe's name from the recipe dictionary

        Args:
            recipe_dict: Dictionary object containing the entire recipe

        Returns:
            A string with the recipe's name if the name tag exists
            An empty string if the name can not be found
        """

        recipe_name = ''
        if 'name' in recipe_dict:
            recipe_name = recipe_dict['name'].strip()

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
            image_url = recipe_dict['image']['url']

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

        recipe_data_json = soup.find('script', type='application/ld+json')
        if recipe_data_json is not None:
            for item in recipe_data_json:
                json_dict = json.loads(item.string)
                for json_item in json_dict:
                    if json_item['@type'] == 'Recipe':
                        recipe_data['name'] = self.extract_recipe_name(json_item)
                        recipe_data['recipeInstructions'] = self.extract_instructions(json_item)
                        recipe_data['recipeIngredient'] = self.extract_ingredients(json_item)
                        recipe_data['image'] = self.extract_recipe_image_url(json_item)

        else:
            recipe_data['name'] = ''
            recipe_data['recipeInstructions'] = ''
            recipe_data['recipeIngredient'] = ''
            recipe_data['image'] = ''

        return recipe_data
