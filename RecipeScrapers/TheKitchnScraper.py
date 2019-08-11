class TheKitchnScraper():
    """This class is responsible for extracting recipe data
    from the kitchn.com
    """

    @staticmethod
    def extract_recipe_name(soup):
        """Extracts the recipe's name from the soup object

        Args:
            soup: Beautiful Soup object containing the recipe data

        Returns:
            A string with the recipe's name
        """

        return soup.find('h2', class_='Recipe__title').string

    @staticmethod
    def extract_ingredients(soup):
        """Extracts the ingredients from the soup object

        Args:
            soup: Beautiful Soup object containing the recipe data

        Returns:
            The list of ingredients
        """

        ingredients = []
        ingredient = ''

        # Find all of the ingredients and add them to the ingredient list
        # Ingredient quantiy and text are seperated by span tags, so this
        # function will have to combine all of the text between span tags.
        for ingredient_class in soup.find_all('li', class_='Recipe__ingredient'):
            for ingredient_item in ingredient_class.find_all('span'):
                ingredient += ingredient_item.get_text()
            ingredients.append(ingredient.strip())
            ingredient = ''

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

        for instruction in soup.find_all('li', class_='Recipe__instruction-step'):
            instructions += '{}\n'.format(instruction.string)

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
        recipe_soup = soup.find('div', class_='Recipe')
        recipe_data['name'] = self.extract_recipe_name(recipe_soup)
        recipe_data['recipeIngredient'] = self.extract_ingredients(recipe_soup)
        recipe_data['recipeInstructions'] = self.extract_instructions(recipe_soup)
        return recipe_data
