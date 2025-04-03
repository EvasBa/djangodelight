from django.shortcuts import render
from .forms import IngridientForm, MenuItemForm, PurchaseForm, RecipeRequirementForm
from .models import Ingridient, MenuItem, Purchase, RecipeRequirements
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

# homepage view
def HomeView(request):
    context = {"Title": "Django Delights"}
    context['MenuItems'] = MenuItem.objects.all()
    return render(request, 'inventory/home.html', context)

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

class IngridientCreateView(CreateView):
    model = Ingridient
    form_class = IngridientForm
    template_name = 'inventory/ingridient_create.html'
    

    def form_valid(self, form):
        # Check if the ingredient already exists
        name = form.cleaned_data['name']
        if Ingridient.objects.filter(name=name).exists():
            form.add_error('name', 'This ingredient already exists.')
            return self.form_invalid(form)
        return super().form_valid(form)

# Ingridient delete view
class IngridientDeleteView(DeleteView):
    model = Ingridient
    template_name = 'inventory/ingridient_confirm_delete.html'
    success_url = '/ingridients/'    


class IngridientUpdateView(UpdateView):
    model = Ingridient
    form_class = IngridientForm
    template_name = 'inventory/ingridient_update.html'


# Purchase class view
class PurchaseListView(ListView):
    model = Purchase
    template_name = 'inventory/purchase_list.html'
    context_object_name = 'purchases'

class PurchaseCreateView(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'inventory/purchase_create.html'

    def form_valid(self, form):
        # Check if the purchase can be made based on stock availability
        menu_item = form.cleaned_data['menu_item']
        quantity = form.cleaned_data['quantity']
        enough_stock = form.instance.enough_stock()
        if not enough_stock:
            form.add_error('menu_item', 'Not enough stock for this purchase.')
            return self.form_invalid(form)
        else:
            # Deduct the stock from the ingredients
            recipe_requirements = RecipeRequirements.objects.filter(menu_item=menu_item)
            for requirement in recipe_requirements:
                ingredient = requirement.ingredient
                ingredient.quantity -= requirement.quantity * quantity
                ingredient.save()
        return super().form_valid(form)

# MenuItem class view
class MenuItemListView(ListView):
    model = MenuItem
    template_name = 'inventory/menu_item_list.html'
    context_object_name = 'menu_items'

class MenuItemCreateView(CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'inventory/menu_item_create.html'

    def form_valid(self, form):
        # Check if the menu item already exists
        title = form.cleaned_data['title']
        if MenuItem.objects.filter(title=title).exists():
            form.add_error('title', 'This menu item already exists.')
            return self.form_invalid(form)
        return super().form_valid(form)


# RecipeRequirements class view
class RecipeRequirementsListView(ListView):
    model = RecipeRequirements
    template_name = 'inventory/recipe_requirements_list.html'
    context_object_name = 'recipe_requirements'

class RecipeRequirementsCreateView(CreateView):
    model = RecipeRequirements
    form_class = RecipeRequirementForm
    template_name = 'inventory/recipe_requirements_create.html'

    def form_valid(self, form):
        # Check if the recipe requirement already exists
        menu_item = form.cleaned_data['menu_item']
        ingredient = form.cleaned_data['ingredient']
        if RecipeRequirements.objects.filter(menu_item=menu_item, ingredient=ingredient).exists():
            form.add_error('ingredient', 'This recipe requirement already exists.')
            return self.form_invalid(form)
        return super().form_valid(form)



# Report class view 
class ReportView(TemplateView):
    template_name = 'inventory/report.html'
    
    def get_context_data(salf, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_revenue'] = sum([purchase.get_total_revenue() for purchase in Purchase.objects.all()])
        context['total_cost'] = sum([purchase.get_total_cost() for purchase in Purchase.objects.all()])
        context['total_profit'] = context['total_revenue'] - context['total_cost']
        context['total_purchases'] = Purchase.objects.count()
        return context