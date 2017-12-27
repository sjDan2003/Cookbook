# Both of these libraries are used to connect and read data from a website.
# Python 3.X uses urllib.request, and Python 2.X uses urllib2

from RecipeMgr import RecipeClass
import xml.etree.ElementTree as et
import re
from xml.etree.ElementTree import ElementTree

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


def WriteRecipeList(newRecipe):

    tree = ElementTree()
    root = et.Element('Cookbook')
    recipe = et.SubElement(root, 'Recipe', attrib=newRecipe.__dict__)
   # et.SubElement(recipe, 'Name', value=newRecipe.GetName())

    # et.dump(root)

    ElementTree(root).write('test.xhtml')

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
    return (re.sub(' +', ' ', recipeText[startIndex:endIndex].strip().replace('",', '').replace('"', '').replace('\n', '')))

#------------------------------------------------------------------------------------------------
