from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count

def indexPage(request, col=4):
   context = {}
   if request.user.is_authenticated: # girişliyse True değer döndürür
      profile = UserInfo.objects.get(user=request.user)
      context.update({"profile":profile})
   category_count = Product.objects.values('category__title','category__slug').annotate(product=Count('title'))
   categorys = Category.objects.all()
   products = Product.objects.all() # Hepsini getir (liste bazlıdır) (for) []
   # products = Product.objects.filter() # (category=telefon) (liste bazlıdır) (for) []
   # products = Product.objects.get() # tek obje 
      
   if request.method == "GET":
      submit = request.GET.get("submit") # ""
      if submit:
         products = products.filter(category__slug = submit)
   

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
   
   context.update({ # sayfa içerisine bilgileri gönderir
      "products":products,
      "col":col,
      "categorys": categorys,
      "category_count": category_count,
   })
   return render(request, 'index.html', context)


def detailPage(request, id):
   product = Product.objects.get(id=id)
   comments = Comment.objects.filter(product=product)
   boolcom = True
   if request.user.is_authenticated:
      userinfo = UserInfo.objects.get(user=request.user)
      boolcom = not Comment.objects.filter(product=product, user=userinfo).exists()
      
   if request.method == "POST":
      if request.user.is_authenticated:
         submit = request.POST.get("submit")
         if submit == "commentForm":
            rating = request.POST.get("rating")
            text = request.POST.get("text")
            if rating is None:
               rating = 5
            
            comment = Comment(rating=rating, text=text, user=userinfo, product=product)
            comment.save()
         elif submit == "shopForm":
            piece = request.POST.get("piece")
            
            if 1 <= int(piece) <= int(product.stok): 
               if not Shoping.objects.filter(user=request.user, product=product).exists():
                  shop = Shoping(user=request.user, product=product, piece=piece)
               else:
                  shop = Shoping.objects.filter(user=request.user, product=product).get()
                  if (int(shop.piece)+int(piece)) <= int(product.stok):
                     shop.piece += int(piece)
                  else:
                     messages.warning(request, 'maximum ürün adetini aştınız. ekleyebileceğiniz ürün adeti: '+str(int(product.stok)-int(shop.piece)))
               shop.save()
            else:
               messages.warning(request, 'İstenilen adet değeri buunmuyor!!')
            
         
         return redirect("/detay/"+id)
      
   context = {
       "product": product,
       "comments": comments,
       "boolcom": boolcom,
   }
   if request.user.is_authenticated:
      context.update({"profile": UserInfo.objects.get(user=request.user)})
   return render(request, 'detail.html', context)


# === PRODUCT ===

def shopPage(request):
   shop = Shoping.objects.filter(user=request.user)
   total_price = 0
   
   for i in shop:
      total_price += i.price
   
   if request.method == "POST":
      print(request.POST)
      index = 0
      for k,v in request.POST.items():
         if "csrfmiddlewaretoken" not in k and "submit" not in k:
            print(k,v)
            if index%2 == 0:
               shoping = shop.get(id=v)
            elif index%2 == 1:
               if int(shoping.product.stok) >= int(v):
                  shoping.piece = v
               else:
                  messages.warning(request, shoping.product.title+' ürünün stok sayısını aştınız. max:'+ str(shoping.product.stok))
               
            shoping.save()
            index +=1
      return redirect("shopPage")

      
   
   context = {
      "shop":shop,
      "total_price": total_price,
   }
   if request.user.is_authenticated:
      context.update({"profile": UserInfo.objects.get(user=request.user)})
   return render(request, 'shoping.html',context)

# ÜRÜN SİLME
def shopDelete(request, id):
   shoping = Shoping.objects.filter(id=id)
   if shoping.exists():
      shoping = shoping.get()
   shoping.delete()
   return redirect("shopPage")

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
      product = products.get(id=productid)  # değiştirilcek ürün
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
   if request.user.is_authenticated:
      context.update({"profile": UserInfo.objects.get(user=request.user)})
   return render(request, 'user/myproduct.html', context)


def delProduct(request, id=None):
   if id is not None:
      product = Product.objects.get(id=id)
      # product = get_object_or_404(Product, id=id) # ürünü getiremezse 404 sayfasına atar
      product.delete()
   else:
      "hata mesajı"
   return redirect("myProduct")


def addProduct(request):
   categorys = Category.objects.all()
   if request.method == "POST":
      title = request.POST.get("title")
      price = request.POST.get("price")
      stok = request.POST.get("stok")
      discount_per = request.POST.get("discount_per")
      text = request.POST.get("text")
      slugcate = request.POST.get("category")  # telefon
      image = request.FILES.get("image")
      category = categorys.get(slug=slugcate)  # id=5 slug=telefon

      product = Product(title=title, oldprice=price, stok=stok, category=category,
                        text=text, image=image, user=request.user)
      if discount_per:
         product.discount_per = discount_per
      product.save()
      return redirect("indexPage")

   context = {
       "categorys": categorys,
   }
   if request.user.is_authenticated:
      context.update({"profile": UserInfo.objects.get(user=request.user)})

   return render(request, 'user/add-product.html', context)

# === USER ===
# PROFILE
def profileUser(request):
   profile = UserInfo.objects.get(user=request.user)
   user = User.objects.get(username=request.user)
   
   if request.method == "POST":
      submit = request.POST.get("submit")  
      if submit == "profileUpdate":
         fname = request.POST.get("name")
         lname = request.POST.get("surname")
         email = request.POST.get("email")
         username = request.POST.get("username")
         address = request.POST.get("address")
         tel = request.POST.get("tel")
         job = request.POST.get("job")
         image = request.FILES.get("image")
         
         
         user.first_name = fname
         user.last_name = lname
         user.email = email
         if not User.objects.filter(username=username).exists(): # ["qqq1"] = not True, []= not False
            user.username = username
            messages.success(request, "Kullanıcı adınız başarıyla değiştirildi..")
         else:
            messages.warning(request, "Bu kullanıcı adı zaten kullanılıyor!")
         
         if image is not None:
            profile.img = image
         profile.address = address
         profile.tel = tel
         profile.job = job

      if submit == "passwordChange":
         password = request.POST.get("password")
         if user.check_password(password): # şifre kontrolü
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if password1 == password2:
               user.set_password(password1) # şifre değiştirme
               profile.password = password1
               login(request,user)
               messages.success(request, "Şifreniz başarıyla değiştirildi..")
            else:
               messages.warning(request, "şifreler eşleşmiyor!")
         else:
            messages.warning(request, "şifreniz yanlış!")
         
      user.save()
      profile.save()
      return redirect('profileUser')
      
   context = {
      "profile":profile,
   }
   return render(request,'user/profile.html', context)


def loginUser(request):

   if request.method == "POST":
      username = request.POST.get("username")
      password = request.POST.get("password")
      
      user = authenticate(username=username, password=password) # bulamazsa None

      if user is not None:
         login(request,user)
         messages.success(request, 'Hoşgeldiniz '+ user.username)
         return redirect("indexPage")
      else:
         messages.warning(request, 'Kullanıcı adı veya şifre yanlış!!')
         return redirect("loginUser")
         
   context = {}
   if request.user.is_authenticated:
      context.update({"profile": UserInfo.objects.get(user=request.user)})
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
               
               userinfo = UserInfo(user=user, password = password1)
               userinfo.save()
               
               messages.success(request, 'Kaydınız başarıyla oluşturuldu..')
               return redirect("loginUser")
            else:
               messages.warning(request, 'Bu mail zaten kullanılıyor!!')
               return redirect("registerUser")
         else:
            messages.warning(request, 'Bu kullanıcı adı daha önceden alınmış!!')
            return redirect("registerUser")
      else:
         messages.warning(request, 'Şifreler aynı değil!!')
         return redirect("registerUser")
      
   context = {}
   if request.user.is_authenticated:
      context.update({"profile": UserInfo.objects.get(user=request.user)})
   return render(request,'user/register.html',context)

def logoutUser(request):
   logout(request)
   return redirect("loginUser")