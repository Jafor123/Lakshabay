from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.urls import reverse

from App_Payment.models import *
from App_Lakshabay.models import *


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    item = models.ForeignKey(gift, on_delete=models.CASCADE, blank=True, null=True)
    item2 = models.ForeignKey(Fitem, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.item != None:
            return f'{self.quantity} X {self.item}'
        else:
            return f'{self.quantity} X {self.item2}'

    def get_total(self):
        if self.item != None:
            total = self.item.gift_price * self.quantity
            float_total = format(total, '0.2f')
            return float_total
        else:
            total = self.item2.item_price * self.quantity
            float_total = format(total, '0.2f')
            return float_total


class TempCart(models.Model):
    user_id = models.BigIntegerField()
    item = models.ForeignKey(gift, on_delete=models.CASCADE, blank=True, null=True)
    item2 = models.ForeignKey(Fitem, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.item != None:
            return f'{self.quantity} X {self.item}'
        else:
            return f'{self.quantity} X {self.item2}'

    def get_total(self):
        if self.item != None:
            total = self.item.gift_price * self.quantity
            float_total = format(total, '0.2f')
            return float_total
        else:
            total = self.item2.item_price * self.quantity
            float_total = format(total, '0.2f')
            return float_total


class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=264, blank=True, null=True)
    orderId = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '{}'.format(str(self.user))

    def get_cart_count(self):
        return self.orderitems.count()

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        return total

    def get_absolute_url(self):
        return reverse("App_Payment:payment", args=[self.id])

class TempOrder(models.Model):
    orderitems = models.ManyToManyField(TempCart)
    user_id = models.BigIntegerField()
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=264, blank=True, null=True)
    orderId = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_cart_count(self):
        return self.orderitems.count()

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        return total


		
class OrderDetail(models.Model):
    product = models.ForeignKey(Order,on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Amount')
    stripe_payment_intent = models.CharField(max_length=200)
    has_paid = models.BooleanField(default=False,verbose_name='Payment Status')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.amount,self.has_paid)		