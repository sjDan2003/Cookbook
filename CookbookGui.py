import os
import json

from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup

from RecipeObject import RecipeObjectClass
from Services import LocalFileServiceClass, GoogleDriveClass, DropboxServiceClass


class ErrorPopUp(Popup):

    """This class creates a popup window which alerts the user
    to an error that has occured.
    """

    errorInfoLabel = ObjectProperty()

    def __init__(self, errorText, **kwargs):
        super(ErrorPopUp, self).__init__(**kwargs)
        self.errorInfoLabel.text = errorText


class RecipeButton(Button):

    """This class manages the buttons in the recycle view.
    """

    def change_recipe(self, recipe_data):
        """ When the user clicks a recipe in the Recipe View Screen, the user should
        expect the Recipe View to change the recipe details to match the recipe they clicked

        Args:
            recipe_data: Objects that stores the parsed recipe data
        """
        app = App.get_running_app()
        recipe_view_screen = app.root.get_screen('recipe view')
        recipe_view_screen.recipe_name.text = recipe_data.get_recipe_name()
        recipe_view_screen.recipe_instructions.text = recipe_data.get_instructions()
        recipe_view_screen.recipe_name.text = recipe_data.get_recipe_name()
        recipe_view_screen.recipe_ingredients.text = ''
        for ingredient in recipe_data.get_ingredients():
            recipe_view_screen.recipe_ingredients.text += '\n{}'.format(ingredient)


class RecipeSaveScreen(Screen):

    """This Recipe Save Screen manages saving and loading parsed recipe
    data from either local files or files in the cloud

    The recipe data is stored in a JSON format"""

    localBaseDir = os.path.split(os.path.abspath(__file__))[0]
    local_recipe_json = os.path.join(localBaseDir, 'RecipeData/savedRecipes.json')

    def load_recipe_data_to_recycle_view(self, recipe_data):
        """Loads the recipe data array into the recycle view.
        Each recipe's name will be the text of each button in
        the recycle view.
        """

        max_button_text_length = 20
        for recpie in recipe_data:
            recipe_object = RecipeObjectClass()
            recipe_object.set_recipe_from_dict(recpie)
            button_text = recipe_object.get_recipe_name()
            if len(button_text) > max_button_text_length:

                button_text = '{}\n{}'.format(button_text[0:max_button_text_length].strip(),
                                              button_text[max_button_text_length:len(button_text)].strip())
            self.manager.get_screen('recipe view').recipeList.data.append({"color": (1, 1, 1, 1),
                                                                           "font_size": "10sp",
                                                                           "text": button_text,
                                                                           "input_data": recipe_object})

    def create_saveable_list(self, recipe_list_data):
        """Takes the recipe dictionary data in the recycle view, and copies
        it to a list that can be saved to a file
        """

        saveable_list = []
        for recipe in recipe_list_data:
            print(recipe)
            saveable_list.append(recipe['input_data'].get_data())
        return saveable_list

    def save_to_local_storage(self):
        """Saves the recipe data to local storage"""

        saveable_list = self.create_saveable_list(self.manager.get_screen('recipe view').recipeList.data)
        local_file_service = LocalFileServiceClass()
        local_file_service.WriteJsonFile(self.local_recipe_json, saveable_list)

        self.manager.transition.direction = 'right'
        self.manager.current = 'recipe view'

    def load_to_local_storage(self):
        """Loads the recipe data from local storage
        and builds the recycle view list
        """

        local_file_service = LocalFileServiceClass()
        loaded_recipe_data = local_file_service.ReadJsonFile(self.local_recipe_json)

        self.load_recipe_data_to_recycle_view(loaded_recipe_data)
        self.manager.transition.direction = 'right'
        self.manager.current = 'recipe view'

    def save_to_google_drive(self):

        """Saves the recipe data to the user's Google Drive
        account
        """

        cloud_service = GoogleDriveClass()

        filename = cloud_service.GetFileName(self.local_recipe_json)
        print(filename)

        if cloud_service.DoesFileExist(filename):

            print('Updating file')
            file_id = cloud_service.GetFileIdFromFilename(filename)
            cloud_service.UpdateFile(file_id, self.local_recipe_json)

        else:

            print('Uploading new file')
            cloud_service.upload_file(self.local_recipe_json)

        cloud_service.PrintFileList()

    def load_from_google_drive(self):
        """Loads recipe data using Google Drive as the source"""

        cloud_service = GoogleDriveClass()
        filename = cloud_service.GetFileName(self.local_recipe_json)

        if cloud_service.DoesFileExist(filename):

            file_id = cloud_service.GetFileIdFromFilename(filename)
            recipe_data = cloud_service.DownloadFile(file_id)
            loaded_recipe_data = json.loads(recipe_data)

            self.load_recipe_data_to_recycle_view(loaded_recipe_data)

        else:

            print("File not found, no data to download")

        self.manager.transition.direction = 'right'
        self.manager.current = 'recipe view'

    def load_from_dropbox(self):
        pass

    def save_to_dropbox(self):
        """Saves the recipe data to local storage before uploading the data
        to the user's Dropbox Account.

        If there is an issue, this function will handle displaying a pop up
        message to the user.

        Args:
            None

        Returns:
            None
        """

        cloud_service = DropboxServiceClass()
        return_message = cloud_service.save_to_dropbox()

        if return_message is not None:
            ErrorPopUp(return_message).open()


class RecipeImportScreen(Screen):

    """The Recipe Import Screen is responsible for creating a new recipe.
    The source of this recipe can be from a URL or the user manually entering
    the recipe details
    """

    url_input = ObjectProperty()
    recipe_name = ObjectProperty()
    recipe_instructions = ObjectProperty()
    recipe_ingredients = ObjectProperty()
    recipe_object = RecipeObjectClass()

    def import_recipe(self):

        """Creates a new recipe object from a URL and shows the data in the Recipe Import Screen
        """

        self.recipe_object.get_recipe_data_from_url(self.url_input.text)

        # Check to see if the new recipe contains valid data.
        # If the URL was invalid or could not connect then don't import the recipe.
        # If the recipe is valid, display the data to the screen.
        if self.recipe_object.is_data_valid():
            self.recipe_name.text = self.recipe_object.get_recipe_name()
            self.recipe_instructions.text = self.recipe_object.get_instructions()
            self.recipe_ingredients.text = ''
            for ingredient in self.recipe_object.get_ingredients():
                self.recipe_ingredients.text += '\n{}'.format(ingredient)

            if len(self.recipe_name.text) > 20:
                self.recipe_name.font_size = "25dp"

        # If there were any errors getting the recipe data, alert the user to what
        # aspects of the recipe are missing.
        recipe_errors = self.recipe_object.get_recipe_errors()
        if recipe_errors != '':
            ErrorPopUp(recipe_errors).open()

    def cancel_recipe_import(self):

        """ Cancel importing a new recipe. Clear all of the fields before returning
        to the Recipe View Screen"""
        self.url_input.text = ''
        self.recipe_name.text = ''
        self.recipe_instructions.text = ''
        self.recipe_ingredients.text = ''
        self.manager.transition.direction = 'right'
        self.manager.current = 'recipe view'

    def confirm_recipe_import(self):

        """Add the imported recipe object to the recipe list and return to the Recipe View Screen"""

        recipe_view_screen = self.manager.get_screen('recipe view')

        # Update the ListView to include the new recipe
        new_recipe_object = RecipeObjectClass(self.recipe_object)
        button_text = new_recipe_object.get_recipe_name()
        if len(button_text) > 20:
            button_text = '{}\n{}'.format(button_text[0:20].strip(),
                                          button_text[20:len(button_text)].strip())
        recipe_view_screen.recipeList.data.append({"color": (1, 1, 1, 1),
                                                   "font_size": "10sp",
                                                   "text": button_text,
                                                   "input_data": new_recipe_object})

        # Update the current view with the new recipe
        recipe_view_screen.recipe_name.text = self.recipe_object.get_recipe_name()

        # Transition back to the recipe view screen
        self.manager.transition.direction = 'right'
        self.manager.current = 'recipe view'


class RecipeViewScreen(Screen):

    """The Recipe View Screen is the primary screen of the app.
    This is where the user is brought to when the app is first loaded.
    """
    recipe_list = ObjectProperty()
    recipe_name = ObjectProperty()
    recipe_instructions = ObjectProperty()
    recipe_ingredients = ObjectProperty()

    def show_save_recipes_screen(self):

        """Displays the Save Recipe Screen.

        This screen will allow the user to save their recipies to local storage
        or to a user's cloud storage
        """

        self.manager.transition.direction = 'right'
        self.manager.current = 'recipe save'

    def show_import_recipe_screen(self):

        """Displays the Recipe Import Screen

        This screen will allow the user to import a recipe from a URL
        """

        recipe_import_screen = self.manager.get_screen('recipe import')
        recipe_import_screen.url_input.text = ''
        recipe_import_screen.recipe_name.text = ''
        recipe_import_screen.recipe_instructions.text = ''
        recipe_import_screen.recipe_ingredients.text = ''
        self.manager.transition.direction = 'left'
        self.manager.current = 'recipe import'


class CookbookGuiApp(App):

    """This is the main class for the Kivy Gui
    """

    def build(self):

        """Builds the Kivy Gui by by creating the screen manager
        """

        cookboox_screen_manager = ScreenManager()
        cookboox_screen_manager.add_widget(RecipeViewScreen())
        cookboox_screen_manager.add_widget(RecipeImportScreen())
        cookboox_screen_manager.add_widget(RecipeSaveScreen())
        return cookboox_screen_manager
