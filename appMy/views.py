from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

def indexPage(request, col=4):
   products = Product.objects.all() # Hepsini getir (liste bazlıdır) (for) []
   # products = Product.objects.filter() # (category=telefon) (liste bazlıdır) (for) []
   # products = Product.objects.get() # tek obje 

   if request.method == "GET":
      filter_product = request.GET.get("filter")
      if filter_product == "1":
         products = products.order_by("price")
      elif filter_product == "2":
         products = products.order_by("-price")
      elif filter_product == "3":
         products = products.order_by("-id")
      elif filter_product == "4":
         products = products.order_by("title")
      elif filter_product == "5":
         products = products.order_by("-title")
         
      
   
   context = { # sayfa içerisine bilgileri gönderir
      "products":products,
      "col":col,
   }
   return render(request, 'index.html', context)


def detailPage(request, id):
   product = Product.objects.get(id=id)
   
   context = {
       "product": product,
   }
   return render(request, 'detail.html', context)

# === USER ===
def myProduct(request):
   products = Product.objects.filter(user=request.user)
   if request.method == "POST":
      # Form içerisinden bilgileri çekme
      title = request.POST.get("title")
      price = request.POST.get("price")
      stok = request.POST.get("stok")
      text = request.POST.get("text")
      image = request.FILES.get("image")
      # Ürünü Getirme
      productid = request.POST.get("productid")
      product = products.get(id=productid) # değiştirilcek ürün
      # Ürün değerlerini değiştirme
      product.title = title
      product.price = price
      product.stok = stok
      product.text = text
      if image is not None:
         product.image = image
      
      product.save()
      return redirect("myProduct")
   
   context = {
       "products": products,
   }
   return render(request, 'user/myproduct.html', context)

def delProduct(request,id=None):
   if id is not None:
      product = Product.objects.get(id=id)
      # product = get_object_or_404(Product, id=id) # ürünü getiremezse 404 sayfasına atar
      product.delete()
   else:
      "hata mesajı"
   return redirect("myProduct")

def addProduct(request):
   if request.method == "POST":
      title = request.POST.get("title")
      price = request.POST.get("price")
      stok = request.POST.get("stok")
      text = request.POST.get("text")
      image = request.FILES.get("image")
      
      product = Product(title=title, price=price, stok=stok, text=text,image=image, user=request.user)
      product.save()
      return redirect("indexPage")
   
   context = {}
   return render(request, 'user/add-product.html', context)

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
   
   if request.method == "POST":
      fname=request.POST.get("fname")
      lname=request.POST.get("lname")
      username=request.POST.get("username")
      email=request.POST.get("email")
      password1=request.POST.get("password1")
      password2=request.POST.get("password2")
      
      if password1 == password2:
         if not User.objects.filter(username=username).exists(): # exists filterda değer varsa True yoksa False döndürür
            if not User.objects.filter(email=email).exists():
               user = User.objects.create_user(username = username, password=password1, email=email,first_name=fname, last_name=lname )
               user.save()
               return redirect("loginUser")
               
   context = {}
   return render(request,'user/register.html',context)

def logoutUser(request):
   logout(request)
   return redirect("loginUser")