# Generated by Django 3.2 on 2021-08-17 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Lakshabay', '0004_alter_menu_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu_category',
            name='file',
            field=models.FileField(default='bell-pepper-capsicum.svg', upload_to='Menuicon/'),
        ),
    ]
