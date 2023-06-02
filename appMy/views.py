from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, logout, authenticate

def indexPage(request):
   products = Product.objects.all() # Hepsini getir (liste bazlıdır) (for) []
   # products = Product.objects.filter() # (category=telefon) (liste bazlıdır) (for) []
   # products = Product.objects.get() # tek obje 
   context = { # sayfa içerisine bilgileri gönderir
      "products":products,
   }
   return render(request, 'index.html', context)


def detailPage(request, id):
   product = Product.objects.get(id=id)
   
   context = {
       "product": product,
   }
   return render(request, 'detail.html', context)


def loginUser(request):

   if request.method == "POST":
      username = request.POST.get("username")
      password = request.POST.get("password")
      
      user = authenticate(username=username, password=password) # bulamazsa None

      if user is not None:
         login(request,user)
         return redirect("indexPage")
      
   context = {}
   return render(request,'user/login.html',context)

def registerUser(request):
   context = {}
   return render(request,'user/register.html',context)