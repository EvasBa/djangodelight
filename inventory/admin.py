from django.contrib import admin
from .models import Ingridient, MenuItem, Purchase, RecipeRequirements

# Register your models here.
@admin.register(Ingridient)
class IngridientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit', 'unit_price')
    search_fields = ('name',)
