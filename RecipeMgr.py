import xml.sax


class RecipeClass(xml.sax.ContentHandler):

    def __init__(self, recipeList=None):

        self._Name = ''
        self._IngredientList = {}
        self._Instructions = ''

        if recipeList != None:

            self._Name = recipeList['_Name']
            self._IngredientList = recipeList['_IngredientList']
            self._Instructions = recipeList['_Instructions']

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
