from django.urls import path
from . import views


app_name="owner"
urlpatterns = [
    path("home/",views.home, name="home"),
    path("homepage/",views.homepage, name="homepage"),
    path("login/",views.ownerlogin,name="login"),
    path("register/",views.registerUser,name="register"),
    path("logout/",views.logoutowner,name="logout"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("registerdish/",views.registerdish,name="registerdish"),
    path("details/<slug:disher>",views.details,name="details"),
    path("cart/",views.cart,name="cart"),
    path("dish/",views.dishmaker,name="dish"),
    path("payment/",views.paydish,name="pay"),
    path("userorder/",views.userorder,name="userorder"),
    path("orderupdate/",views.orderupdate,name="orderupdate"),
    path("hisorder/",views.hisorder,name="hisorder"),




]






