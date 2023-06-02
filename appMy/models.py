from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
   user = models.ForeignKey(User, verbose_name=("Kullanıcı - Satıcı"), on_delete=models.CASCADE)
   title = models.CharField(("Başlık"), max_length=50)
   text = models.TextField(("İçerik"))
   image = models.FileField(("Ürün Resmi"), upload_to='product', max_length=100)
   date_now = models.DateField(("Tarih"), auto_now_add= True)
   stok = models.IntegerField(("Stok"))
   price = models.FloatField(("Ürün Fiyatı"))
   
   
   def __str__(self): # admin panelndeki isimlendirmeyi değiştirir
      return self.title