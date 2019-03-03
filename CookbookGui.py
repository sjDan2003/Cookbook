from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout


class CookbookLayout(GridLayout):
    recipeList = ObjectProperty()
    recipeName = ObjectProperty()

    def ChangeRecipeName(self):
        self.recipeName.text = 'Porterhouse Steak'


class CookbookGuiApp(App):
    def build(self):
        return CookbookLayout()
