import cookbook as cb
from RecipeMgr import RecipeClass
import xml.etree.ElementTree as et

urlAddress = 'http://www.foodnetwork.com/recipes/ina-garten/sauteed-broccolini-and-garlic-recipe.html'
urlText = cb.GetUrlText(urlAddress)

newRecipe = RecipeClass()

recipieText = cb.GetRecipeText(urlText)

newRecipe.SetName(cb.GetRecipeName(recipieText))
print(newRecipe.GetName())

newRecipe.SetIngredientList(cb.GetIngredients(recipieText))
ingredList = newRecipe.GetIngredientList()
ingredListLen = len(ingredList) // 3
for index in range(ingredListLen):
    print('{} {} {}'.format(ingredList['quantity' + str(index)], ingredList['units' + str(index)], ingredList['ingredient' + str(index)]))

recipeInstructions = cb.GetRecipeInstructions(recipieText)
print(recipeInstructions)
newRecipe.SetInstructions(recipeInstructions)
cb.WriteRecipeList(newRecipe)
xmlRecipeList = None
with open('test.xhtml', 'r') as file:
    tree = et.parse(file)
    root = tree.getroot()
    for child in root:
        xmlRecipeList = child.attrib

print(xmlRecipeList['_Name'])
xmlRecipe = RecipeClass(xmlRecipeList)
print(xmlRecipe.GetIngredientList())


print('Hello World')
