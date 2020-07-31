import json
from .AllRecipeScraper import AllRecipesScraper

class CookingLightScraper(AllRecipesScraper):
    """This class is responsible for extracting recipe data
    from cookinglight.com
    """

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
            instructions = recipe_dict['recipeInstructions']

        return instructions
