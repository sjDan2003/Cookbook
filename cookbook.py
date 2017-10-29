# Both of these libraries are used to connect and read data from a website.
# Python 3.X uses urllib.request, and Python 2.X uses urllib2

from RecipeMgr import RecipeClass
import json

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

#------------------------------------------------------------------------------------------------

def GetUrlText(urlAddress):

    urlRequest = urllib2.Request(urlAddress)
    urlResponse = urllib2.urlopen(urlRequest)
    urlText = urlResponse.read()

    # In Python 2.X, reading from a response returns a string, but in Python 3.X it returns raw bytes
    # This causes problems when the rest of this program is expecting a string
    # Determine if the text is a string, if it isn't then decode the binary data into a string.

    if not isinstance(urlText, str):
        urlText = urlText.decode()

    return urlText

def WriteRecipeList(recipeList):

    with open('RecipeList.json', 'w') as outPtr:
        json.dump(recipeList.__dict__, outPtr)


#------------------------------------------------------------------------------------------------

def GetRecipeText(urlText):

    startText = 'script type="application/ld+json">'
    endText = '"review": ['
    startIndex = urlText.find(startText)
    endIndex = urlText.find(endText, startIndex)
    return(urlText[startIndex:endIndex])

def GetRecipeAttr(recipieText, targetStr):

    startIndex = recipieText.find(targetStr) + len(targetStr)
    endIndex = recipieText.find('"', startIndex)
    return (recipieText[startIndex:endIndex])

def GetRecipeName(recipieText):

    return (GetRecipeAttr(recipieText, '"name": "'))

def IsValidUnit(measuringUnit):

    validMeasuringUnits = {'tablespoon', 'tablespoons', 'teaspoon', 'teaspoons' 'bunch', 'bunches', 'cup', 'cups'}
    return (measuringUnit in validMeasuringUnits)

def GetIngredients(recipieText):

    startIndex = recipieText.find('"recipeIngredient": [') + len('"recipeIngredient": [')
    endIndex = recipieText.find(']', startIndex)
    tempIngList = recipieText[startIndex:endIndex].strip().splitlines()
    ingLen = len(tempIngList)
    ingredList = {}
    for index in range(ingLen):

        ingredText = tempIngList[index].strip()

        # Get the quantity of the ingredient
        startIndex = 1
        endIndex = ingredText.find(' ', startIndex)
        ingredList['quantity' + str(index)] = ingredText[startIndex:endIndex]

        # Get the measuring unit of the ingredient
        startIndex = endIndex + 1
        endIndex = ingredText.find(' ', startIndex)
        ingredList['units' + str(index)] = ''
        if IsValidUnit(ingredText[startIndex:endIndex]):

            ingredList['units' + str(index)] = ingredText[startIndex:endIndex]

        else:

            endIndex = startIndex - 1

        # Get the ingredient name
        startIndex = endIndex - 1
        endIndex = ingredText.find('"', startIndex)
        ingredList['ingredient' + str(index)] = ingredText[startIndex + 2 : endIndex]

    return ingredList

def GetRecipeInstructions(recipeText):

    startIndex = recipeText.find('recipeInstructions": [') + len('recipeInstructions": [')
    endIndex = recipeText.find(']', startIndex)
    return (recipeText[startIndex:endIndex].strip().replace('"', '').replace('\n', ' '))

#------------------------------------------------------------------------------------------------

urlAddress = 'http://www.foodnetwork.com/recipes/ina-garten/sauteed-broccolini-and-garlic-recipe.html'
urlText = GetUrlText(urlAddress)
recipieText = GetRecipeText(urlText)
newRecipe = RecipeClass()

newRecipe.SetRecipeName(GetRecipeName(recipieText))
print(newRecipe.GetRecipeName())

newRecipe.SetIngredientList(GetIngredients(recipieText))
ingredList = newRecipe.GetIngredientList()
ingredListLen = len(ingredList) // 3
for index in range(ingredListLen):
    print('{} {} {}'.format(ingredList['quantity' + str(index)], ingredList['units' + str(index)], ingredList['ingredient' + str(index)]))

recipeInstructions = GetRecipeInstructions(recipieText)
print(recipeInstructions)
WriteRecipeList(newRecipe)
