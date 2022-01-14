from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class BillingAddress(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=264)
    address2 = models.CharField(max_length=265,blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    aditional_info = models.TextField(blank=True, default="additional information")

    def __str__(self):
        return f'{self.firstname} billing address'

    def is_fully_filled(self):
        field_names = [f.name for f in self._meta.get_fields()]

        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True

    class Meta:
        verbose_name_plural = "Billing Addresses"