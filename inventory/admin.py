from django.contrib import admin
from .models import Ingridient, MenuItem, Purchase, RecipeRequirements, CustomUser

# Register your models here.
@admin.register(Ingridient)
class IngridientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit', 'unit_price')
    search_fields = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price_perunit', 'description', 'picture')
    search_fields = ('title',)

@admin.register(RecipeRequirements)
class RecipeRequirementsAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'ingredient', 'quantity')
    search_fields = ('menu_item__title', 'ingredient__name')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'time_stamp', 'quantity')
    search_fields = ('menu_item__title',)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('email',)
    add_fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2')
        }),
    )
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2')}
        ),
    )