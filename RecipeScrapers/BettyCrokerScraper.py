class BettyCrockerScraper():
    """This class is responsible for extracting recipe data
    from bettycroker.com
    """

    @staticmethod
    def extract_ingredients(soup):
        """Extracts the ingredients from the soup object

        Args:
            soup: Beautiful Soup object containing the recipe data

        Returns:
            The list of ingredients
        """

        ingredients = ''
        for ingredient in soup.find_all('div', class_='recipePartIngredient'):
            quantiy = ingredient.find('div', class_='quantity').get_text().strip()
            description = ingredient.find('div', class_='description').get_text().strip()
            ingredients += '{} {}\n'.format(quantiy, description)
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
        for instuction in soup.find_all('div', class_="recipePartStepDescription"):

            for child in instuction.contents:

                if child.string is not None:
                    instructions += '{}\n'.format(child.string.strip())

        return instructions

    @staticmethod
    def extract_recipe_name(soup):
        """Extracts the recipe's name from the soup object

        Args:
            soup: Beautiful Soup object containing the recipe data

        Returns:
            A string with the recipe's name
        """
        recipe_name = ''
        recipe_tag = soup.find('h1', class_="recipePartTitleText")
        if recipe_tag is not None:
            recipe_name = recipe_tag.string
        return recipe_name

    @staticmethod
    def extract_recipe_image_url(soup):
        """Extracts the recipe's image URL from the recipe dictionary
        This URL will be used to download the image by the main recipe object

        Args:
            recipe_dict: Dictionary object containing the entire recipe

        Returns:
            A string with the recipe's image url if the image tag exists
            An empty string if the name can not be found
        """

        image_url = ''
        image_tag = soup.find('meta', property="og:image")
        if image_tag is not None:
            image_url = image_tag.get('content')
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
        recipe_data['name'] = self.extract_recipe_name(soup)
        recipe_data['recipeIngredient'] = self.extract_ingredients(soup)
        recipe_data['recipeInstructions'] = self.extract_instructions(soup)
        recipe_data['image'] = self.extract_recipe_image_url(soup)
        return recipe_data
