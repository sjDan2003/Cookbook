import os
import json

class RecipeClass:

    workingPath = os.getcwd()
    recipePath = workingPath + '/Recipes'

    def __init__(self, recipeList=None):

        self._Name = ''
        self._IngredientList = {}
        self._Instructions = ''

        if recipeList != None:

            self._Name = recipeList['_Name']
            self._IngredientList = recipeList['_IngredientList']
            self._Instructions = recipeList['_Instructions']

    def jsonDefault(object):
        return object.__dict__

    def SaveRecipe(self):

        if os.path.exists(RecipeClass.recipePath) == False:
            os.mkdir(RecipeClass.recipePath)

        with open('{}/{}.json'.format(RecipeClass.recipePath, self._Name), 'w+') as f:
            json.dump(self, f, default=RecipeClass.jsonDefault)

    def LoadRecipe(self, recipeName):

        with open('{}/{}.json'.format(RecipeClass.recipePath, recipeName), 'r') as f:
            jsonDict = json.load(f)
            self._Name = jsonDict['_Name']
            self._IngredientList = jsonDict['_IngredientList']
            self._Instructions = jsonDict['_Instructions']

    def SetName(self, recipeName):

        self._Name = recipeName

    def GetName(self):

        return (self._Name)

    def SetIngredientList(self, ingredList):

        self._IngredientList = ingredList

    def GetIngredientList(self):

        return (self._IngredientList)

    def SetInstructions(self, instructions):

        self._Instructions = instructions

    def GetInstructions(self):

        return (self._Instructions)
