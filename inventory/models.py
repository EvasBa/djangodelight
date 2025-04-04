from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    '''
    Custom manager for the CustomUser model.
    '''
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_approved', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_approved') is not True:
            raise ValueError('Superuser must have is_approved=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    '''
    Custom user model for the restaurant application.
    '''
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# Create your models here.
class Ingridient(models.Model):
    '''
    Represents a single ingredient in the restaurant's inventory
    '''
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=10)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return '/ingridients'
    
class MenuItem(models.Model):
    '''
    Represents an entry off the restaurant's menu'
    '''
    title = models.CharField(max_length=100)
    price_perunit = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    picture = models.ImageField(upload_to='menu_pictures/', blank=True, null=True)

    def __str__(self):
        return self.title
    
    

class RecipeRequirements(models.Model):
    '''
    Represents an ingredient required for a recipe for a MenuItem
    '''
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingridient, on_delete=models.CASCADE)
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
    
    def enough_stock(self):
        recipe_requirements = RecipeRequirements.objects.filter(menu_item=self.menu_item)
        for requirement in recipe_requirements:
            if requirement.ingredient.quantity < requirement.quantity * self.quantity:
                return False
        return True
    
    
    def get_total_revenue(self):
        return self.menu_item.price_perunit * self.quantity
    
    def get_total_cost(self):
        total_cost = 0
        recipe_requirements = RecipeRequirements.objects.filter(menu_item=self.menu_item)
        for requirement in recipe_requirements:
            total_cost += requirement.ingredient.unit_price * requirement.quantity
        return total_cost
    
    def get_absolute_url(self):
        return "/purchases"