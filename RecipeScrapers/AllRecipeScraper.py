class AllRecipesScraper():
    """This class is responsible for extracting recipe data
    from allrecipes.com
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
        for ingredient in soup.find_all('span', itemprop="recipeIngredient"):
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
        for instuction in soup.find_all('span', class_="recipe-directions__list--item"):
            instructions += '{}\n'.format(instuction.string)
        return instructions

    @staticmethod
    def extract_recipe_name(soup):
        """Extracts the recipe's name from the soup object

        Args:
            soup: Beautiful Soup object containing the recipe data

        Returns:
            A string with the recipe's name
        """

        return soup.find('h1', id="recipe-main-content").string

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
