from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
   title = models.CharField(("Kategori"), max_length=50)
   slug = models.SlugField(("Slug"), blank=True) # türkçe karakterleri ve boşlukları(-) dönüştürür

   def save(self, *args, **kwargs): # bir model kaydedildiğinde içerdeki kodları çalıştırır sonra tekrar kaydeder
      self.slug = slugify(self.title)
      super().save(*args, **kwargs)

   def __str__(self):  # admin panelndeki isimlendirmeyi değiştirir
      return self.title
   
   
class Product(models.Model):
   user = models.ForeignKey(User, verbose_name=("Kullanıcı - Satıcı"), on_delete=models.CASCADE)
   category = models.ForeignKey(Category, verbose_name=("Kategori"), on_delete=models.CASCADE, null=True)
   title = models.CharField(("Başlık"), max_length=50)
   text = models.TextField(("İçerik"))
   image = models.FileField(("Ürün Resmi"), upload_to='product', max_length=100)
   date_now = models.DateField(("Tarih"), auto_now_add= True)
   stok = models.IntegerField(("Stok"))
   oldprice = models.FloatField(("Eski Fiyat"), null=True)
   discount_per = models.IntegerField(("İndirim Yüzdesi"),blank=True ,null=True, default=0)
   price = models.FloatField(("İndirimli Fiyatı"), blank=True, null=True)
   # 1) eski ve yeni fiyat yazarız aradaki indirimi yüzdeyle hesaplatırıcaz
   # 2) eski fiyatı ve indirim yüzdesini yazarım, yeni fiyata indirimli fiyatı yazdırırız
   
   def __str__(self): # admin panelndeki isimlendirmeyi değiştirir
      return self.title
   
   def save(self,*args, **kwargs):
      if self.discount_per:
         self.price = round(self.oldprice - ((self.oldprice * self.discount_per)/100), 2)
      else:
         self.price = self.oldprice
      super().save(*args,**kwargs)
   
class UserInfo(models.Model):
   user = models.ForeignKey(User, verbose_name=("Kulanıcı"), on_delete=models.CASCADE)
   password = models.CharField(("Şifre"), max_length=50)
   address = models.TextField(("Adres"), default="-")
   tel = models.CharField(("Telefon"), max_length=50, default="-")
   img = models.ImageField(("Profil Resmi"), upload_to="profile", default="profile/default-profile.png")
   job = models.CharField(("İş"), max_length=50, default="-")
   
   def __str__(self):  # admin panelndeki isimlendirmeyi değiştirir
      return self.user.username

