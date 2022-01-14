from django.urls import path
from App_Order import views

app_name = 'App_Order'

urlpatterns = [
    path('add/<pk>/', views.add_to_cart, name="add"),
    path('remove/<pk>/', views.remove_from_cart, name="remove"),
    path('cart/', views.cart_view, name="cart"),
    path('increase/<pk>/', views.increase_cart, name="increase"),
    path('decrease/<pk>/', views.decrease_cart, name="decrease"),

    path('add-food/<pk>/', views.item_add_to_cart, name="item_ad"),
    path('item-cart/', views.item_cart_view, name="item_cart"),
    path('item-increase/<pk>/', views.itemincrease_cart, name="item_increase"),
    path('item-decrease/<pk>/', views.itemdecrease_cart, name="item_decrease"),
    path('item-remove/<pk>/', views.itemremove_from_cart, name="item_remove"),


]
