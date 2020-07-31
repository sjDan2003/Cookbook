from django.db import models
from django.urls import reverse

class Recipe(models.Model):
    name = models.CharField(max_length=50)
    ingredients = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return self.name

    def form_valid(self, form):
        """
            This overloaded function can provide checks on
            the recipe to make sure it's formatted correctly
            and correct information is entered.
        """
        return super().form_valid(form)

    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'pk':self.pk})


