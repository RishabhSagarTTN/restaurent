# Generated by Django 5.1.6 on 2025-03-26 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0002_alter_dishes_dish_veg'),
    ]

    operations = [
        migrations.AddField(
            model_name='dishes',
            name='dish_detail',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='dish_veg',
            field=models.CharField(choices=[('Veg', 'Vegitarian'), ('Non Veg', 'Non Vegitarian')], default='Veg', max_length=10),
        ),
    ]
