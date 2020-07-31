from django.urls import path

from . import views
from .views import RecipeListView, RecipeDetailView, RecipeCreateView, RecipeUpdateView

urlpatterns = [
    path('', RecipeListView.as_view(), name='index'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/new/', RecipeCreateView.as_view(), name='recipe-create'),
    path('recipe/<int:pk>/update', RecipeUpdateView.as_view(), name='recipe-update'),
    path('NewRecipe/', views.NewRecipeView, name='NewRecipe'),
]