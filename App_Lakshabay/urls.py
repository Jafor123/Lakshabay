from django.urls import path
from App_Lakshabay import views
app_name='App_Lakshabay'
urlpatterns = [
    path('',views.index,name='index'),
    path('menu/', views.MenuView, name='menus'),
    path('onlineorder/', views.onlineorder, name='onlineorder'),
    path('gifts/', views.GiftView, name='gifts'),
    path('book/', views.Bookview, name='book'),
    path('contact-us',views.ContactusView,name='contactus'),
    path('gallery/', views.GalleryView, name='gallery_image'),
]
