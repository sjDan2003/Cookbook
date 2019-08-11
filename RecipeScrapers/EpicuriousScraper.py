import json

class EpicuriousScraper():
    """This class is responsible for extracting recipe data
    from epicurious.com
    """

    @staticmethod
    def extract_recipe_name(soup):
        """Extracts the recipe's name from the soup object

        One of the places where the recipe name is stored on epicurious is
        in a variable called digital data. This variable stores a dictionary object
        containing not only the recipe name, but other information that could be
        useful in the future.

        Args:
            soup: Beautiful Soup object containing the recipe data

        Returns:
            A string with the recipe's name
        """

        recipe_name = ''
        for item in soup.find_all('script', type='text/javascript'):
            search_string = 'var digitalData = '
            if search_string in item.string:

                # Removing leading and trailing whitespace around the item
                item_string = item.string.strip()

                # Strip the variable name out of the string
                digital_data_var = item_string[len(search_string):(len(item_string) - 1)]

                # Convert the string to a dict
                json_digital_data = json.loads(digital_data_var)
                recipe_name = json_digital_data['display']
                break

        return recipe_name

    @staticmethod
    def extract_ingredients(soup):
        """Extracts the ingredients from the soup object

        Args:
            soup: Beautiful Soup object containing the recipe data

        Returns:
            The list of ingredients
        """

        ingredients = []

        for ingredient in soup.find_all('li', class_='ingredient'):
            ingredients.append(ingredient.string)

        return ingredients

    @staticmethod
    def extract_instructions(soup):
        """Extracts the recipe instructions from the soup object

        Args:
            soup: Beautiful Soup object containing the recipe data

        Returns:
            A string with the recipe instructions
        """

        instructions = ''

        for instruction in soup.find_all('li', class_='preparation-step'):
            instructions += '{}\n'.format(instruction.string.strip())

        return instructions

    def extract_recipe_data(self, soup):
        """Manages the collection of all recipe data and returns that
        data back to the calling function.

        Args:
            soup: Beautiful Soup object containing the recipe data

        Returns:
            A dictionary containing all of the relevant recipe data
        """

        recipe_data = {}
        recipe_data['name'] = self.extract_recipe_name(soup)
        recipe_data['recipeIngredient'] = self.extract_ingredients(soup)
        recipe_data['recipeInstructions'] = self.extract_instructions(soup)
        return recipe_data
