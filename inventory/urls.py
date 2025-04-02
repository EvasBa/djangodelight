from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView, name="home"),
    path("ingridients/", views.IngridientListView.as_view(), name="ingridient_list"),
    path("purchases/", views.PurchaseListView.as_view(), name="purchases_list"),
    path("menu/", views.MenuItemListView.as_view(), name="menu_item_list"),
    path("reciperequirement/", views.RecipeRequirementsListView.as_view(), name="recipe_requirements_item_list"),
]

