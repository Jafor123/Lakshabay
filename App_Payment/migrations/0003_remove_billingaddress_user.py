# Generated by Django 3.2 on 2021-08-16 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Payment', '0002_auto_20210816_1914'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='user',
        ),
    ]
