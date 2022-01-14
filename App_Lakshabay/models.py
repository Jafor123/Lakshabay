from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
# Create your models here.
class contact(models.Model):
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=240, blank=False)
    phone = models.CharField(max_length=20, blank=False)
    message = models.TextField(max_length=300, blank=False)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return '{}-{}'.format(self.name, self.timestamp.date())




class gallery(models.Model):
    gallery_id = models.AutoField(primary_key=True)
    gallery_name = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to="images/", blank=True)

    def __str__(self):
        return self.gallery_name

    class Meta:
        verbose_name = _("Gallery")
        verbose_name_plural = _("Gallery")


class category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=120, blank=False)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


SELECT_GIFT_CAT_TYPE = (
    ('Voucher', 'Voucher'),
    ('Product', 'Product'),
)


class gift(models.Model):
    gift_id = models.AutoField(primary_key=True)
    gift_name = models.CharField(max_length=120, blank=False)
    gift_sl_no = models.CharField(max_length=120, blank=True)
    gift_category = models.ForeignKey(category, on_delete=models.CASCADE)
    gift_type = models.CharField(choices=SELECT_GIFT_CAT_TYPE, max_length=150)
    gift_meta = models.CharField(max_length=255, blank=False)
    gift_description = models.TextField()
    gift_image = models.ImageField(upload_to="gifts/", blank=False)
    gift_price = models.IntegerField(blank=True, null=True)
    gift_weight = models.IntegerField(blank=True, null=True)
    gift_dimension = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.gift_name


class menu_category(models.Model):
    menu_cat_id = models.AutoField(primary_key=True)
    menu_cat_name = models.CharField(max_length=120, blank=False)
    file=models.FileField(upload_to="Menuicon/",default="bell-pepper-capsicum.svg")

    def __str__(self):
        return self.menu_cat_name

    class Meta:
        verbose_name = _("Menu Category")
        verbose_name_plural = _("Menu Categories")


class Fitem(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=120, blank=False)
    item_category = models.ForeignKey(menu_category, on_delete=models.CASCADE)
    item_description = models.TextField()
    item_price = models.FloatField(blank=True, null=True)
    photo = models.ImageField(upload_to="Online Food", default='defaultfood.jpg')

    def __str__(self):
        return self.item_name


class book(models.Model):
    book_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=120, blank=False)
    last_name = models.CharField(max_length=120, blank=False)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(null=True, blank=True, default=None)
    phone = models.CharField(max_length=13, blank=False)
    email = models.EmailField(max_length=120, blank=False)
    number_of_people = models.IntegerField(blank=True, null=True)
    message = models.TextField()

    def __str__(self):
        return str(self.book_id)

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("book")


class menu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    menu_name = models.CharField(max_length=120, blank=False)
    category = models.ForeignKey(menu_category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to="Menu/",default="defaultfood.jpg", blank=True)

    def __str__(self):
        return self.menu_name