from django.shortcuts import render
from .forms import IngridientForm, MenuItemForm, PurchaseForm, RecipeRequirementForm
from .models import Ingridient, MenuItem, Purchase, RecipeRequirements
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# homepage view
def HomeView(request):
    cntxt = {"Title": "Django Delights"}
    return render(request, 'inventory/home.html', cntxt)

# Ingridient class view
class IngridientListView(ListView):
    model = Ingridient
    template_name = 'inventory/ingridient_list.html'
    context_object_name = 'ingridients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_ingridients'] = Ingridient.objects.count()
        context['total_value']= sum([ing.quantity * ing.unit_price for ing in Ingridient.objects.all()])
        return context
    

# Purchase class view
class PurchaseListView(ListView):
    model = Purchase
    template_name = 'inventory/purchase_list.html'
    context_object_name = 'purchases'

# MenuItem class view
class MenuItemListView(ListView):
    model = MenuItem
    template_name = 'inventory/menu_item_list.html'
    context_object_name = 'menu_items'


# RecipeRequirements class view
class RecipeRequirementsListView(ListView):
    model = RecipeRequirements
    template_name = 'inventory/recipe_requirements_list.html'
    context_object_name = 'recipe_requirements'