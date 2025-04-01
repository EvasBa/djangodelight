from django.db import models

# Create your models here.
class Ingridients(models.Model):
    '''
    Represents a single ingredient in the restaurant's inventory
    '''
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=10)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str(self):
        return self.name
    
class MenuItem(models.Model):
    '''
    Represents an entry off the restaurant's menu'
    '''
    title = models.CharField(max_length=100)
    price_perunit = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    picture = models.ImageField(upload_to='menu_pictures/')

    def __str__(self):
        return self.title

class RecipeRequirements(models.Model):
    '''
    Represents an ingredient required for a recipe for a MenuItem
    '''
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingridients, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.menu_item} - {self.ingredient}"
    
class Purchase(models.Model):
    '''
    Represents a purchase of a menu item
    '''
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.menu_item} - {self.time_stamp}"