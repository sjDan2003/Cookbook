class EatingWellScraper():
    """This class is responsible for extracting recipe data
    from eatingwell.com
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
        for ingredient in soup.find_all('span', itemprop='ingredients'):
            ingredients.append(ingredient.string.strip())
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
        for instuction in soup.find_all('span', class_="recipeDirectionsListItem"):
            # Eating well has an extra recipe direction that has no text and doesn't
            # pertain to the instructions.
            # If this attribute is found ignore it.
            if 'ng-bind-html' not in instuction.attrs:
                instructions += '{}\n'.format(instuction.string.strip())
        return instructions

    @staticmethod
    def extract_recipe_name(soup):
        """Extracts the recipe's name from the soup object

        Args:
            soup: Beautiful Soup object containing the recipe data

        Returns:
            A string with the recipe's name
        """

        return soup.find('meta', property='og:title')['content']

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
