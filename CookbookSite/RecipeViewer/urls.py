from django.urls import path

from . import views
from .views import (
    RecipeListView,
    RecipeDetailView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    RecipeSearchView
)

urlpatterns = [
    path('', RecipeListView.as_view(), name='index'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/new/', RecipeCreateView.as_view(), name='recipe-create'),
    path('recipe/<int:pk>/update/', RecipeUpdateView.as_view(), name='recipe-update'),
    path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe-delete'),
    path('search/', RecipeSearchView.as_view(), name='recipe-search'),
    path('NewRecipe/', views.new_recipe_view, name='NewRecipe'),
]
