from django.shortcuts import render
from .forms import IngridientForm, MenuItemForm, PurchaseForm, RecipeRequirementForm
from .models import Ingridient, MenuItem, Purchase, RecipeRequirements
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView

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

class ReportView(TemplateView):
    template_name = 'inventory/report.html'
    
    def get_context_data(salf, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_revenue'] = sum([purchase.get_total_revenue() for purchase in Purchase.objects.all()])
        context['total_cost'] = sum([purchase.get_total_cost() for purchase in Purchase.objects.all()])
        context['total_profit'] = context['total_revenue'] - context['total_cost']
        context['total_purchases'] = Purchase.objects.count()
        return context