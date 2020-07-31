from django import forms

class NewRecipeForm(forms.Form):
    recipe_url = forms.CharField(label='Recipe URL', required=True)
