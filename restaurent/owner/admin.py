from django.contrib import admin
from .models import Dishes

# Register your models here.
# admin.site.register(Orders)
# admin.site.register(Review)

class BlogPostAdmin(admin.ModelAdmin):
    list_display=('dish_name','dish_category','price',)
    list_filter=('price',)
    search_fields=('dish_name','dish_category',)
    list_per_page=10
    prepopulated_fields = {"dish_sluger": ("dish_name",)}


admin.site.register(Dishes,BlogPostAdmin)