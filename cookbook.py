import urllib2

def GetRecipeAttr(targetStr):
    startIndex = urlText.find(targetStr) + len(targetStr)
    endIndex = urlText.find('"', startIndex)
    return (urlText[startIndex:endIndex])

urlAddress  = 'http://www.foodnetwork.com/recipes/ina-garten/sauteed-broccolini-and-garlic-recipe.html'
urlRequest  = urllib2.Request(urlAddress)
urlResponse = urllib2.urlopen(urlRequest)
urlText     = urlResponse.read()

startText = 'script type="application/ld+json">'
endText = '"review": ['
startIndex = urlText.find(startText)
endIndex = urlText.find(endText, startIndex)
urlText = urlText[startIndex:endIndex]



recipeName = GetRecipeAttr('"name": "')
print(recipeName)
startIndex = urlText.find('"recipeIngredient": [') + len('"recipeIngredient": [')
endIndex = urlText.find(']', startIndex)
tempIngList = urlText[startIndex:endIndex].strip().splitlines()
print(tempIngList)
ingLen = len(tempIngList)
ingredList = {}
for index in range(ingLen):
    ingred = tempIngList[index].strip()
    startIndex = ingred.find('"') + 1
    endIndex = ingred.find('"', startIndex)
    ingredList['quantity'+str(index)] = ingred[startIndex:startIndex+1]
    ingredList['ingredient'+str(index)] = ingred[startIndex + 2 : endIndex]

ingredListLen = len(ingredList) // 2
for index in range(ingredListLen):
    print('{} {}'.format(ingredList['quantity'+str(index)], ingredList['ingredient'+str(index)]))