import os
import json

from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

from WebsiteScraper import RecipeObjectClass
from Services import LocalFileServiceClass, GoogleDriveClass, DropboxServiceClass


class ErrorPopUp(Popup):

    errorInfoLabel = ObjectProperty()

    def __init__(self, errorText, **kwargs):
        super(ErrorPopUp, self).__init__(**kwargs)
        self.errorInfoLabel.text = errorText


class RecipeButton(Button):

    def ChangeRecipe(self, recipeData):
        """ When the user clicks a recipe in the Recipe View Screen, the user should
        expect the Recipe View to change the recipe details to match the recipe they clicked

        Args:
            recipeData: Objects that stores the parsed recipe data
        """
        app = App.get_running_app()
        app.root.get_screen('recipe view').recipeName.text = recipeData.GetRecipeName()
        app.root.get_screen('recipe view').recipeInstructions.text = recipeData.GetInstructions()
        app.root.get_screen('recipe view').recipeName.text = recipeData.GetRecipeName()
        app.root.get_screen('recipe view').recipeIngredients.text = ''
        for ingredient in recipeData.GetIngredients():
            app.root.get_screen('recipe view').recipeIngredients.text += '\n{}'.format(ingredient)


class RecipeSaveScreen(Screen):

    """This Recipe Save Screen manages saving and loading parsed recipe
    data from either local files or files in the cloud

    The recipe data is stored in a JSON format"""

    localBaseDir = os.path.split(os.path.abspath(__file__))[0]
    localRecipeJson = os.path.join(localBaseDir, 'RecipeData/savedRecipes.json')

    def LoadRecipeDataToRecycleView(self, recipeData):

        for recpie in recipeData:
            recipObj = RecipeObjectClass()
            recipObj.SetRecipeFromDict(recpie)
            buttonText = recipObj.GetRecipeName()
            if len(buttonText) > 20:
                buttonText = '{}\n{}'.format(buttonText[0:20].strip(), buttonText[20:len(buttonText)].strip())
            self.manager.get_screen('recipe view').recipeList.data.append({"color": (1, 1, 1, 1), "font_size": "10sp", "text": buttonText, "input_data": recipObj})

    def CreateSaveableList(self, recipeListData):
        """Takes the recipe dictionary data in the recycle view, and copies
        it to a list that can be saved to a file
        """

        saveableList = []
        for recipe in recipeListData:
            print(recipe)
            saveableList.append(recipe['input_data'].GetData())
        return saveableList

    def SaveToLocalStorage(self):
        """Saves the recipe data to local storage"""

        saveableList = self.CreateSaveableList(self.manager.get_screen('recipe view').recipeList.data)
        localFileService = LocalFileServiceClass()
        localFileService.WriteJsonFile(self.localRecipeJson, saveableList)

        self.manager.transition.direction = 'right'
        self.manager.current = 'recipe view'

    def LoadFromLocalStorage(self):
        """Loads the recipe data from local storage
        and builds the recycle view list
        """

        localFileService = LocalFileServiceClass()
        loadedRecipeData = localFileService.ReadJsonFile(self.localRecipeJson)

        self.LoadRecipeDataToRecycleView(loadedRecipeData)
        self.manager.transition.direction = 'right'
        self.manager.current = 'recipe view'

    def SaveToGoogleDrive(self):

        cloudService = GoogleDriveClass()

        print(self.localRecipeJson)

        filename = cloudService.GetFileName(self.localRecipeJson)
        print(filename)

        if cloudService.DoesFileExist(filename):

            print('Updating file')
            fileId = cloudService.GetFileIdFromFilename(filename)
            cloudService.UpdateFile(fileId, self.localRecipeJson)

        else:

            print('Uploading new file')
            cloudService.UploadFile(self.localRecipeJson)

        cloudService.PrintFileList()

    def LoadFromGoogleDrive(self):
        """Loads recipe data using Google Drive as the source"""

        cloudService = GoogleDriveClass()
        filename = cloudService.GetFileName(self.localRecipeJson)

        if cloudService.DoesFileExist(filename):

            fileId = cloudService.GetFileIdFromFilename(filename)
            recipeData = cloudService.DownloadFile(fileId)
            loadedRecipeData = json.loads(recipeData)

            self.LoadRecipeDataToRecycleView(loadedRecipeData)

        else:

            print("File not found, no data to download")

        self.manager.transition.direction = 'right'
        self.manager.current = 'recipe view'

    def LoadFromDropbox(self):
        pass

    def SaveToDropbox(self):
        pass


class RecipeImportScreen(Screen):
    """The Recipe Import Screen is responsible for creating a new recipe.
    The source of this recipe can be from a URL or the user manually entering
    the recipe details
    """

    urlInput = ObjectProperty()
    recipeName = ObjectProperty()
    recipeInstructions = ObjectProperty()
    recipeIngredients = ObjectProperty()
    recipeObj = RecipeObjectClass()

    def ImportRecipe(self):

        """Creates a new recipe object from a URL and shows the data in the Recipe Import Screen
        """

        self.recipeObj.GetRecipeFromUrl(self.urlInput.text)

        # Check to see if the new recipe contains valid data.
        # If the URL was invalid or could not connect then don't import the recipe.
        # If the recipe is valid, display the data to the screen.
        if self.recipeObj.validData:
            self.recipeName.text = self.recipeObj.GetRecipeName()
            self.recipeInstructions.text = self.recipeObj.GetInstructions()
            self.recipeIngredients.text = ''
            for ingredient in self.recipeObj.GetIngredients():
                self.recipeIngredients.text += '\n{}'.format(ingredient)

            if len(self.recipeName.text) > 20:
                self.recipeName.font_size = "25dp"

        # If there were any errors getting the recipe data, alert the user to what
        # aspects of the recipe are missing.
        recipeErrors = self.recipeObj.GetRecipeErrors()
        if recipeErrors != '':
            ErrorPopUp(recipeErrors).open()

    def CancelRecipeImport(self):

        """ Cancel importing a new recipe. Clear all of the fields before returning
        to the Recipe View Screen"""
        self.urlInput.text = ''
        self.recipeName.text = ''
        self.recipeInstructions.text = ''
        self.recipeIngredients.text = ''
        self.manager.transition.direction = 'right'
        self.manager.current = 'recipe view'

    def ConfirmRecipeImport(self):

        """Add the imported recipe object to the recipe list and return to the Recipe View Screen"""

        # Update the ListView to include the new recipe
        newRecipeObj = RecipeObjectClass(self.recipeObj)
        buttonText = newRecipeObj.GetRecipeName()
        if len(buttonText) > 20:
            buttonText = '{}\n{}'.format(buttonText[0:20].strip(), buttonText[20:len(buttonText)].strip())
        self.manager.get_screen('recipe view').recipeList.data.append({"color": (1, 1, 1, 1), "font_size": "10sp", "text": buttonText, "input_data": newRecipeObj})

        # Update the current view with the new recipe
        self.manager.get_screen('recipe view').recipeName.text = self.recipeObj.GetRecipeName()

        # Transition back to the recipe view screen
        self.manager.transition.direction = 'right'
        self.manager.current = 'recipe view'


class RecipeViewScreen(Screen):

    """The Recipe View Screen is the primary screen of the app.
    This is where the user is brought to when the app is first loaded.
    """
    recipeList = ObjectProperty()
    recipeName = ObjectProperty()
    recipeInstructapions = ObjectProperty()
    recipeIngredients = ObjectProperty()

    def ShowSaveRecipesScreen(self):

        self.manager.transition.direction = 'right'
        self.manager.current = 'recipe save'

    def ShowImportRecipeScreen(self):

        self.manager.get_screen('recipe import').urlInput.text = ''
        self.manager.get_screen('recipe import').recipeName.text = ''
        self.manager.get_screen('recipe import').recipeInstructions.text = ''
        self.manager.get_screen('recipe import').recipeIngredients.text = ''
        self.manager.transition.direction = 'left'
        self.manager.current = 'recipe import'


class CookbookGuiApp(App):

    def build(self):
        cookbooxScreenManager = ScreenManager()
        cookbooxScreenManager.add_widget(RecipeViewScreen())
        cookbooxScreenManager.add_widget(RecipeImportScreen())
        cookbooxScreenManager.add_widget(RecipeSaveScreen())
        return cookbooxScreenManager
