# Generated by Django 5.1.6 on 2025-03-21 08:19

import customer.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=50)),
                ('customer_age', models.CharField(max_length=50)),
                ('customer_food', models.CharField(max_length=50)),
                ('customer_Phoneno', models.IntegerField(validators=[customer.models.phonevalidator])),
                ('customer_time', models.DateTimeField()),
            ],
        ),
    ]
