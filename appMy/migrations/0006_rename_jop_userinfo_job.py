# Generated by Django 4.1.5 on 2023-06-07 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appMy', '0005_alter_userinfo_address_alter_userinfo_img_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='jop',
            new_name='job',
        ),
    ]
