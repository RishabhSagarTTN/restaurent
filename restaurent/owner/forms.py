from django import forms
from .models import Dishes
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinLengthValidator
from django.core.validators import EmailValidator
import re
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


def validate_password(value):
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters.")
    if not re.search(r"[A-Z]", value): 
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r"[0-9]", value):  
        raise ValidationError("Password must contain at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
        raise ValidationError("Password must contain at least one special character.")
    return value

def validate_age(value):
    if value < 10 or value > 100:
        raise ValidationError("Age must be between 10 and 100.")
    return value

class Register(forms.Form):
    """Registration form model which is used to  grenerate the user registration form with  proper validation checks """
    Name = forms.CharField(max_length=100, required=True)
    Age = forms.IntegerField(required=True, validators=[validate_age],
                             widget=forms.NumberInput(attrs={"type": "number", "placeholder": "0"}))
    Password = forms.CharField(widget=forms.PasswordInput, required=True, validators=[validate_password])
    Confirm = forms.CharField(widget=forms.PasswordInput, required=True)
    Email = forms.EmailField(required=True, validators=[EmailValidator()])

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('Password')
        confirm_password = cleaned_data.get('Confirm')

        if password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data


class LoginUser(forms.Form):
    """Login User form model which is   used to generate the login form with proper validation checks"""
    user=forms.CharField(required=True,widget=forms.TextInput(attrs={"class":"email"}))
    password=forms.CharField(required=True,widget=forms.PasswordInput)
    
    def clean_user(self):
        user = self.cleaned_data.get("user")
        if not user.isalnum():
            raise ValidationError("Username should only contain letters and numbers.")
        
        if not User.objects.filter(username=user).exists():
            raise ValidationError("This username does not exist.")
        
        return user

    def clean(self):
        """Cross-field validation to check user authentication."""
        cleaned_data = super().clean()
        user = cleaned_data.get("user")
        password = cleaned_data.get("password")

        
        user_obj = authenticate(username=user, password=password)
        if not user_obj:
            raise ValidationError("Invalid username or password.")
        return cleaned_data


class registrationDish(forms.ModelForm):
    """RegistrationDish form model which is used to generate the registration of Dish form with proper checks"""
    dish_sluger=forms.SlugField(widget=forms.TextInput(attrs={"type":"hidden"}),required=False)

    class Meta:
        model=Dishes
        fields=['dish_name','price','dish_category','dish_image','dish_sluger','dish_quantity','dish_veg','dish_detail']
        
        widgets={
            "dish_detail":forms.Textarea(attrs={"placeholder": "If not given then auto populated by AI if it is famous dish"}),
        }    


    def clean_dish_name(self):
        dish_name = self.cleaned_data.get('dish_name')
        if not dish_name:
            raise ValidationError("Dish name cannot be empty.")
        return dish_name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price

    def clean_dish_quantity(self):
        dish_quantity = self.cleaned_data.get('dish_quantity')
        if dish_quantity < 0:
            raise ValidationError("Dish quantity cannot be negative.")
        return dish_quantity

    def clean_dish_sluger(self):
        dish_name = self.cleaned_data.get('dish_name')
        dish_sluger = self.cleaned_data.get("dish_sluger")
        if dish_name:
            dish_sluger = slugify(dish_name)
        return dish_sluger
    

class searching(forms.Form):
    """It is the form for seraching """
    searching_data = forms.CharField(max_length=100, required=False, validators=[MinLengthValidator(1)])

    def clean_searching_data(self):
        data = self.cleaned_data.get('searching_data')
        if data and len(data.strip()) < 1:
            raise ValidationError("Search term cannot be empty or just whitespace.")
        return data


    




