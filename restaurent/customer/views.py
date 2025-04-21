from django.shortcuts import render
from django.http.response import HttpResponse

def home(request):
    return HttpResponse("hello")
    # return render(request,"customer/home.html")


