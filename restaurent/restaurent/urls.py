from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from  . import views

admin.site.site_title="Restaurent Management"
admin.site.index_title="Dish Portal"
admin.site.site_header="Restaurent Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("customer/",include("customer.urls")),
    path("owner/",include("owner.urls")),
    path("",views.home)
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



urlpatterns += [
    path('silk/', include('silk.urls')),
]
# urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

