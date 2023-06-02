# Generated by Django 4.1.5 on 2023-05-31 07:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Başlık')),
                ('text', models.TextField(verbose_name='İçerik')),
                ('image', models.FileField(upload_to='product', verbose_name='Ürün Resmi')),
                ('date_now', models.DateField(auto_now_add=True, verbose_name='Tarih')),
                ('stok', models.IntegerField(verbose_name='Stok')),
                ('price', models.FloatField(verbose_name='Ürün Fiyatı')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı - Satıcı')),
            ],
        ),
    ]
