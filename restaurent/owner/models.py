from django.db import models
from django.contrib.auth.models import User
from .customeManager import CustomeSortedManager
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


choices=[('Veg','Vegitarian'),('Non Veg', 'Non Vegitarian')]


def validate_dish_name(value):
    if not value:
        raise ValidationError("Dish name cannot be empty.")
    if len(value) < 3:
        raise ValidationError("Dish name must be at least 3 characters long.")
    return value


class Dishes(models.Model):
    """Dish model"""
    dish_name = models.CharField(primary_key=True, max_length=50, unique=False, validators=[validate_dish_name])
    price = models.IntegerField(default=0, validators=[MinValueValidator(1)])  
    dish_category = models.CharField(max_length=50,blank=False) 
    dish_image = models.ImageField(default="image.png")
    dish_sluger = models.SlugField(max_length=50, default="", null=False)
    dish_veg = models.CharField(max_length=10, choices=choices, default="Veg")
    dish_detail = models.TextField(blank=True)

    dish_quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1)  

    test = CustomeSortedManager()
    objects = models.Manager()

    class Meta:
        app_label="owner"

        

    def __str__(self):
        return f"{self.dish_name} - {self.dish_category} ({self.dish_veg})"

order_status_choices = [('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED'), ('REJECTED', 'REJECTED')]

class Orders(models.Model):
    """Orders model"""
    customerName = models.ForeignKey(User, on_delete=models.CASCADE)  
    customerDish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    corderDate = models.DateTimeField()
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)]) 
    status = models.CharField(max_length=50, blank=True, choices=order_status_choices)  

    class Meta:
        app_label="owner"
    
    def total(self):
        return self.quantity * self.customerDish.price

    def clean(self):
        """Custom validation to ensure that total price calculation is correct"""
        if self.quantity <= 0:
            raise ValidationError("Quantity must be a positive number.")
        return super().clean()

    def __str__(self):
        return f"{self.customerName} - {self.customerDish} ({self.quantity})"
 

 