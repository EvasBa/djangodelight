from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView, name="home"),
    path("ingridients/", views.IngridientListView.as_view(), name="ingridient_list"),
]

