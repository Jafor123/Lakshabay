# Generated by Django 3.1.6 on 2021-08-21 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Payment', '0003_remove_billingaddress_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]