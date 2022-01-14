from django.contrib import admin
from App_Order.models import *
# Register your models here.
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(TempOrder)
admin.site.register(TempCart)
admin.site.register(OrderDetail)