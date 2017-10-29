class RecipeClass:

    _RecipeName = None
    _IngredientList = None
    _RecipeInstructions = None

    def __init__(self):
        self._RecipeName = ''
        self._IngredientList = {}
        self._RecipeInstructions = ''

    def SetRecipeName(self, recipeName):

        self._RecipeName = recipeName

    def GetRecipeName(self):

        return (self._RecipeName)

    def SetIngredientList(self, ingredList):

        self._IngredientList = ingredList

    def GetIngredientList(self):

        return (self._IngredientList)
