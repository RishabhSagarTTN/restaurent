from django.db import models
from django.core.exceptions import ValidationError
import re

def phonevalidator(value):
    """validating the phone number"""
    pattern = r'^\+?(\d{1,4})?[\s.-]?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{1,4}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid phone number format.')
    
class Customer(models.Model):
     """customer model"""
     customer_name=models.CharField(max_length=50)
     customer_age=models.CharField(max_length=50)
     customer_food=models.CharField(max_length=50)
     customer_Phoneno=models.IntegerField(validators=[phonevalidator])
     customer_time=models.DateTimeField()
