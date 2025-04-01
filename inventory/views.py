from django.shortcuts import render
from .forms import IngridientForm, MenuItemForm, PurchaseForm, RecipeRequirementForm
from .models import Ingridient, MenuItem, Purchase, RecipeRequirements
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# homepage view
def HomeView(request):
    cntxt = {"Title": "Django Delights"}
    return render(request, 'inventory/home.html', cntxt)

class IngridientListView(ListView):
    model = Ingridient
    template_name = 'inventory/ingridient_list.html'
    context_object_name = 'ingridients'