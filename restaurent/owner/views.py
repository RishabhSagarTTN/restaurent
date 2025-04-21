import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import Register, LoginUser, registrationDish, searching
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Dishes, Orders
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from .util import AIdata

logger = logging.getLogger(__name__)

def home(request):
    """
    Renders the home page with available dishes, filtering options, and sorting.
    Supports:
        - Displaying distinct dish categories.
        - Filtering by search term or category.
        - Sorting by price ascending/descending.
        - Identifying which dishes are already in the current user's cart (status="").
    """
    cat = Dishes.objects.values('dish_category').distinct()[:5]
    if Orders.objects.select_related("customerName", "customerDish").filter(customerName__username=request.user.username):
        sdata = Orders.objects.select_related("customerName", "customerDish").filter(customerName__username=request.user.username, status="").values_list('customerDish__dish_sluger', flat=True)
    else:
        sdata = []
    searchdata = searching()
    if request.GET.get("searching_data"):
        search = request.GET.get("searching_data")
        search_filter = Q(dish_name__icontains=search) | Q(dish_category__icontains=search) | Q(dish_veg__iexact=search)
        data = Dishes.objects.filter(search_filter)
    elif request.GET.get("selection"):
        fil = request.GET.get("selection")
        data = Dishes.objects.filter(dish_category=fil)
    else:
        data = Dishes.objects.all()
    if request.method == 'POST':
        sor = request.POST.get("sort")
        if sor == "desc":
            data = data.order_by("-price")
        elif sor == "acen":
            data = data.order_by("price")
    return render(request, "owner/home.html", {"data": data, "cat": cat, "searching": searchdata, "sdata": sdata})

def ownerlogin(request):
    """
    Handles the login process for an owner.
    If valid credentials are posted, logs the user in and redirects to the next page or home.
    Otherwise, displays the login form.
    """
    if request.method == "POST":
        data = LoginUser(request.POST)
        if data.is_valid():
            passwords = data.cleaned_data['password']
            users = data.cleaned_data['user']
            user = authenticate(request, username=users, password=passwords)
            if user is not None:
                login(request, user)
                next_url = request.GET.get("next", "/owner/home")
                return redirect(next_url)
    loginForm = LoginUser()
    return render(request, "owner/login.html", {"form": loginForm})

def registerUser(request):
    """
    Handles user registration.
    Validates registration form and creates a new user if the username is not taken.
    Automatically logs in the user after successful registration.
    """
    if request.method == "POST":
        data = Register(request.POST)
        if data.is_valid():
            name = data.cleaned_data['Name']
            age = data.cleaned_data['Age']
            password = data.cleaned_data['Password']
            email = data.cleaned_data['Email']
            if User.objects.filter(username=name).exists():
                messages.error(request, "Username already exists.")
                return redirect("/owner/register")
            user = User.objects.create_user(username=name, email=email, password=password)
            user.save()
            login(request, user)
            return redirect("/owner/home")
        regForm = Register()
        return render(request, "owner/register.html", {"form": data})
    else:
        regForm = Register()
        return render(request, "owner/register.html", {"form": regForm})

@login_required(login_url="/owner/login")
def logoutowner(request):
    """
    Logs out the current user and redirects to the login page.
    """
    logout(request)
    return redirect("/owner/login")

def details(request, disher):
    """
    Displays details of a single dish, including AI-generated metadata or suggestions.
    
    Parameters:
        disher (str): Slug of the dish to retrieve.
    """
    data = Dishes.objects.get(dish_sluger=disher)
    details = AIdata(data, disher)
    return render(request, "owner/detail.html", {"data": data, "details": details})

@login_required(login_url="/owner/login")
@permission_required("owner.add_dishes", raise_exception=True)
def dashboard(request):
    """
    Admin dashboard page accessible only to users with permission to add dishes.
    """
    return render(request, "owner/dashboard.html")

@login_required(login_url="/owner/login")
@permission_required("owner.add_dishes", raise_exception=True)
def registerdish(request):
    """
    Handles dish registration (admin only).
    Allows uploading of dish information and image through a form.
    """
    if request.method == 'POST':
        form = registrationDish(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/owner/home")
        return render(request, "owner/registerdish.html", {"form": form})
    form = registrationDish()
    return render(request, "owner/registerdish.html", {"form": form})

def cart(request):
    """
    Manages the user's cart.
    Allows:
        - Updating quantities of items.
        - Removing items (if quantity is 0).
        - Displays total cost and item list.
    """
    if request.method == 'POST':
        quant = request.POST.get("quantity")
        dishslug = request.POST.get("dish")
        Orders.objects.select_related("customerName", "customerDish").filter(customerDish__dish_sluger=dishslug).update(quantity=quant)
        if quant == '0':
            Orders.objects.filter(customerDish__dish_sluger=dishslug).delete()
    if Orders.objects.filter(customerName__username=request.user.username, status=""):
        sdata = Orders.objects.filter(customerName__username=request.user.username, status="")
        total = [item.total() for item in sdata]
        tempo = zip(sdata, total)
        totalPrice = sum(total)
        return render(request, "owner/cart.html", {"sdata": tempo, "total": totalPrice})
    else:
        return render(request, "owner/cart.html")

@login_required(login_url="/owner/login")
def dishmaker(request):
    """
    Handles addition or deletion of dishes from the order.
    POST supports:
        - Adding a dish to the cart (dish slug).
        - Deleting a dish from the database (admin-only expected usage).
    """
    try:
        userinfo = User.objects.get(username=request.user)
        if request.method == 'POST':
            if request.POST.get("dish"):
                dishinfo = Dishes.objects.get(dish_sluger=request.POST.get("dish"))
                quantity = 1
                temp = Orders(customerName=userinfo, customerDish=dishinfo, corderDate=timezone.now(), quantity=quantity)
                temp.save()
            if request.POST.get("dishDelete"):
                temp = Dishes.objects.filter(dish_sluger=request.POST.get("dishDelete"))
                temp.delete()
        return redirect("/owner/home")
    except Exception as e:
        return render(request, "owner/404.html")

@login_required(login_url="/owner/login")
def paydish(request):
    """
    Marks all items in the current user's cart as 'PENDING'.
    """
    try:
        temp = Orders.objects.filter(customerName__username=request.user.username, status="")
        for temp in temp:
            temp.status = "PENDING"
            temp.save()
        return render(request, "owner/payment.html")
    except Exception as e:
        return render(request, "owner/404.html")

@login_required(login_url="/owner/login")
@permission_required("owner.add_dishes", raise_exception=True)
def userorder(request):
    """
    Admin interface to manage all user orders.
    Features:
        - Accepting or rejecting orders.
        - Displaying order history with total cost.
        - Pagination support.
    """
    try:
        if request.method == "POST":
            if request.POST.get("accept"):
                data = request.POST.get("accept").split("+")
                Orders.objects.filter(customerName__username=data[0], customerDish__dish_name=data[1]).update(status="COMPLETED")
            else:
                data = request.POST.get("reject").split("+")
                Orders.objects.filter(customerName__username=data[0], customerDish__dish_name=data[1]).update(status="REJECTED")
        sdata = Orders.objects.select_related("customerName", "customerDish").order_by("customerName__username").order_by("-corderDate")
        total = [item.total() for item in sdata]
        tempo = list(zip(sdata, total))
        totalPrice = sum(total)
        pagination = Paginator(tempo, per_page=10)
        page = request.GET.get("page")
        if page is not None and int(page) <= 0:
            raise Exception("Something went wrong")
        page_obj = pagination.get_page(page)
        return render(request, "owner/userorder.html", {"sdata": page_obj, "total": totalPrice})
    except Exception as e:
        return render(request, "owner/404.html")

@login_required(login_url="/owner/login")
def hisorder(request):
    """
    Displays the current user's order history, including:
        - Orders with status PENDING, COMPLETED, or REJECTED.
        - Total cost calculation.
        - Pagination for orders.
    """
    try:
        fil = Q(customerName__username=request.user.username) & (Q(status="PENDING") | Q(status="COMPLETED") | Q(status="REJECTED"))
        sdata = Orders.objects.select_related("customerName", "customerDish").filter(fil).order_by("-corderDate")
        total = [item.total() for item in sdata]
        tempo = list(zip(sdata, total))
        totalPrice = sum(total)
        pagination = Paginator(tempo, per_page=10)
        page = request.GET.get("page")
        if page is not None and int(page) <= 0:
            raise Exception("Something went wrong")
        page_obj = pagination.get_page(page)
        return render(request, "owner/hisorder.html", {"sdata": page_obj, "total": totalPrice})
    except Exception as e:
        return render(request, "owner/404.html")

def orderupdate(request):
    """
    Placeholder view for updating orders.
    Currently only renders a static template.
    """
    return render(request, "owner/orderupdate.html")

def homepage(request):
    """
    Displays a basic version of the homepage with a limited list of dishes.
    Used for testing or simplified views.
    """
    cat = Dishes.objects.all()[:5]
    return render(request, "owner/test.html", {"data": cat})
