from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView, name="home"),
    path("ingridients/", views.IngridientListView.as_view(), name="ingridient_list"),
    path("ingridients/new/", views.IngridientCreateView.as_view(), name="ingridient_create"),
    path("ingridients/<int:pk>/delete/", views.IngridientDeleteView.as_view(), name="ingridient_delete"),
    path("ingridients/<int:pk>/update/", views.IngridientUpdateView.as_view(), name="ingridient_update"),
    path("purchases/", views.PurchaseListView.as_view(), name="purchases_list"),
    path("menu/", views.MenuItemListView.as_view(), name="menu_item_list"),
    path("reciperequirement/", views.RecipeRequirementsListView.as_view(), name="recipe_requirements_item_list"),
    path("reports/", views.ReportView.as_view(), name="report"),
]

