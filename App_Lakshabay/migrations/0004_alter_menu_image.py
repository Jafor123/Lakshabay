# Generated by Django 3.2 on 2021-08-17 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Lakshabay', '0003_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='image',
            field=models.ImageField(blank=True, default='defaultfood.jpg', upload_to='Menu/'),
        ),
    ]
