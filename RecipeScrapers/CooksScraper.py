class CooksScraper():
    """This class is responsible for extracting recipe data
    from cooks.com
    """

    @staticmethod
    def extract_ingredients(soup):
        """Extracts the ingredients from the soup object

        Args:
            soup: Beautiful Soup object containing the recipe data

        Returns:
            The list of ingredients
        """

        ingredients = []
        for ingredient in soup.find_all('span', class_="ingredient"):
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

        instructions = soup.find('div', class_='instructions').get_text()
        return instructions

    @staticmethod
    def extract_recipe_name(soup):
        """Extracts the recipe's name from the soup object

        Args:
            soup: Beautiful Soup object containing the recipe data

        Returns:
            A string with the recipe's name
        """

        # The recipe title is captalized for cooks.com
        # When the title is found, make it all lower case then capitalize
        # the first letter of each word before returning the title.

        recipe_name = ''

        for input_attr in soup.find_all('input', attrs={'name': 'title'}):
            if 'value' in input_attr.attrs:
                raw_name = input_attr['value'].lower()
                name = ''
                for word in raw_name.split(' '):
                    name += '{} '.format(word.capitalize())
                    recipe_name = name.strip()
        return recipe_name

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
