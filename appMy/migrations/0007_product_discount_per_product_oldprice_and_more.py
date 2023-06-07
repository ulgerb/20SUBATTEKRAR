# Generated by Django 4.1.5 on 2023-06-07 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appMy', '0006_rename_jop_userinfo_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_per',
            field=models.IntegerField(null=True, verbose_name='İndirim Yüzdesi'),
        ),
        migrations.AddField(
            model_name='product',
            name='oldprice',
            field=models.FloatField(null=True, verbose_name='Eski Fiyat'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(blank=True, null=True, verbose_name='İndirimli Fiyatı'),
        ),
    ]
