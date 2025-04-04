from django import forms
from .models import Ingridient, MenuItem, Purchase, RecipeRequirements, CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

class IngridientForm(forms.ModelForm):
    class Meta:
        model = Ingridient
        fields = "__all__"
        labels = {
            'name': 'Ingredient Name',
            'quantity': 'Quantity',
            'unit': 'Unit',
            'unit_price': 'Unit Price',
        }
        

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__"

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = "__all__"

class RecipeRequirementForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirements
        fields = "__all__"

