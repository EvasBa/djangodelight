from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.HomeView, name="home"),
    path("ingridients/", views.IngridientListView.as_view(), name="ingridient_list"),
    path("ingridients/new/", views.IngridientCreateView.as_view(), name="ingridient_create"),
    path("ingridients/<int:pk>/delete/", views.IngridientDeleteView.as_view(), name="ingridient_delete"),
    path("ingridients/<int:pk>/update/", views.IngridientUpdateView.as_view(), name="ingridient_update"),
    path("purchases/", views.PurchaseListView.as_view(), name="purchases_list"),
    path("purchases/new/", views.PurchaseCreateView.as_view(), name="purchases_create"),
    path("menu/", views.MenuItemListView.as_view(), name="menu_item_list"),
    path("menu/<int:pk>/delete/", views.MenuItemDeleteView.as_view(), name="menu_item_delete"),
    path("menu/<int:pk>/update/", views.MenuItemUpdateView.as_view(), name="menu_item_update"),
    path("menu/new/", views.MenuItemCreateView.as_view(), name="menu_item_create"),
    path("reciperequirement/", views.RecipeRequirementsListView.as_view(), name="recipe_requirements_item_list"),
    path("reciperequirement/new/", views.RecipeRequirementsCreateView.as_view(), name="recipe_requirements_create"),
    path("reports/", views.ReportView.as_view(), name="report"),
    path("accounts/register/", views.register, name="register"),
    path("accounts/logout/", views.log_out, name="logout"),
    path("accounts/login/", views.log_in, name="login"),
]

