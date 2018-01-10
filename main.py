import os

import cookbook as cb
from RecipeMgr import RecipeClass

def ListRecipes():

    print('\n')

    if os.path.exists(RecipeClass.recipePath) == False:
        print('No Recipies Exist')

    recipeList = os.listdir(RecipeClass.recipePath)

    for recipe in recipeList:
        print(recipe[0:len(recipe) - len('.json')])

urlAddress = 'http://www.foodnetwork.com/recipes/rachael-ray/caprese-salad-recipe-1939232'
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

newRecipe.SaveRecipe()
jsonRecipe = RecipeClass()
jsonRecipe.LoadRecipe(newRecipe.GetName())

print(jsonRecipe.GetName())

ListRecipes()
