# Generated by Django 4.1.5 on 2023-06-07 07:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appMy', '0003_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=50, verbose_name='Şifre')),
                ('address', models.TextField(verbose_name='Adres')),
                ('tel', models.CharField(max_length=50, verbose_name='Telefon')),
                ('img', models.ImageField(upload_to='profile', verbose_name='Profil Resmi')),
                ('jop', models.CharField(max_length=50, verbose_name='İş')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kulanıcı')),
            ],
        ),
    ]