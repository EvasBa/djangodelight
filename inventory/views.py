from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import IngridientForm, MenuItemForm, PurchaseForm, RecipeRequirementForm, CustomUserCreationForm
from .models import Ingridient, MenuItem, Purchase, RecipeRequirements
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


def HomeView(request):
    '''Home view for the inventory app'''
    context = {"Title": "Django Delights"}
    context['MenuItems'] = MenuItem.objects.all()
    return render(request, 'inventory/home.html', context)


class IngridientListView(LoginRequiredMixin, ListView):
    '''List view for the Ingridient model'''
    model = Ingridient
    template_name = 'inventory/ingridient_list.html'
    context_object_name = 'ingridients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_ingridients'] = Ingridient.objects.count()
        context['total_value']= sum([ing.quantity * ing.unit_price for ing in Ingridient.objects.all()])
        return context

class IngridientCreateView(LoginRequiredMixin, CreateView):
    '''Create view for the Ingridient model'''
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


class IngridientDeleteView(LoginRequiredMixin, DeleteView):
    '''Delete view for the Ingridient model'''
    model = Ingridient
    template_name = 'inventory/ingridient_confirm_delete.html'
    success_url = '/ingridients/'    


class IngridientUpdateView(LoginRequiredMixin, UpdateView):
    '''Update view for the Ingridient model'''
    model = Ingridient
    form_class = IngridientForm
    template_name = 'inventory/ingridient_update.html'


# Purchase class view
class PurchaseListView(LoginRequiredMixin, ListView):
    '''List view for the Purchase model'''
    model = Purchase
    template_name = 'inventory/purchase_list.html'
    context_object_name = 'purchases'

class PurchaseCreateView(CreateView):
    '''Create view for the Purchase model'''
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


class MenuItemListView(LoginRequiredMixin, ListView):
    '''List view for the MenuItem model'''
    model = MenuItem
    template_name = 'inventory/menu_item_list.html'
    context_object_name = 'menu_items'

class MenuItemCreateView(LoginRequiredMixin, CreateView):
    '''Create view for the MenuItem model'''
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

class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    '''Update view for the MenuItem model'''
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'inventory/menu_item_update.html'

class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    '''Delete view for the MenuItem model'''
    model = MenuItem
    template_name = 'inventory/menu_item_confirm_delete.html'
    success_url = '/menu/'

class RecipeRequirementsListView(LoginRequiredMixin, ListView):
    '''List view for the RecipeRequirements model'''
    model = RecipeRequirements
    template_name = 'inventory/recipe_requirements_list.html'
    context_object_name = 'recipe_requirements'

class RecipeRequirementsCreateView(LoginRequiredMixin, CreateView):
    '''Create view for the RecipeRequirements model'''
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


class ReportView(LoginRequiredMixin, TemplateView):
    '''Report view for the inventory app'''
    template_name = 'inventory/report.html'
    
    def get_context_data(salf, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_revenue'] = sum([purchase.get_total_revenue() for purchase in Purchase.objects.all()])
        context['total_cost'] = sum([purchase.get_total_cost() for purchase in Purchase.objects.all()])
        context['total_profit'] = context['total_revenue'] - context['total_cost']
        context['total_purchases'] = Purchase.objects.count()
        context['purchased_items'] = Purchase.objects.all().order_by('-id')[:5]
        return context

def log_in(request):
    '''Login view for the inventory app'''
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)  # Correct usage
            return redirect('home')  # Redirect to the homepage or another page
        else:
            return render(request, 'inventory/login.html', {'error': 'Invalid email or password'})
    return render(request, 'inventory/login.html')

def log_out(request):
    '''Logout view for the inventory app'''
    logout(request)
    return redirect('home')

def register(request):
    '''Registration view for the inventory app'''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_approved = False
            user.is_staff = False
            user.save()
            messages.success(request, 'Registration successful. Please wait for approval.')
            
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inventory/register.html', {'form': form})