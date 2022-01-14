from django.urls import path
from App_Superadmin import views
app_name="App_Superadmin"
urlpatterns = [
    path('', views.Dashboard, name='dashboard'),
    path('superadmin-login', views.SuperadminLogin, name="superadmin_login"),
    path('superadmin-logout', views.SuperadminLogout, name="superadmin_logout"),


    path('oderlist/',views.Oderlist,name='oderlist'),
    path('view-order-details/<int:id>',views.ViewOrderDetails,name="orderdetails"),
    path('delete-order/<int:id>',views.DeletereOrder,name='delete_order'),

    path('category/', views.CategoryView, name="category"),
    path('delete/<int:id>', views.CatDeleteView, name="category_delete"),
    path('update/<int:id>', views.CatUpdateView, name="category_update"),

    path('menu-category/', views.MunuCategoryView, name="menu-category"),
    path('menu-delete/<int:id>', views.MenuCatDeleteView, name="menu_category_delete"),
    path('menu-update/<int:id>', views.MenuCatUpdateView, name="menu_category_update"),

    path('food-item/', views.FoodItem, name="food_item"),
    path('food-delete/<int:id>', views.FoodItemDeleteView, name="food_item_delete"),
    path('food-update/<int:id>', views.FoodItemUpdateView, name="food_item_update"),

    path('food-gifts/', views.GiftView, name="gift"),
    path('food-gift-update/<int:id>', views.GiftUpdate, name="gift_update"),
    path('food-gift-delete/<int:id>', views.GiftDelete, name="gift_delete"),

    path('gallary-view/', views.Gallaryview, name="gallary"),
    path('gallary-update/<int:id>', views.GallaryUpdate, name="gallary_update"),
    path('gallary-delete/<int:id>', views.GallarytDelete, name="gallary_delete"),

    path('booking/', views.Bookingview, name="booking"),
    path('booking-delete/<int:id>', views.BookingDelete, name="booking_delete"),
    path('booking-update/<int:id>', views.BookingUpdate, name="booking_update"),

    path('profile-view', views.ProfileView, name="profile"),
    path('profile-delete/<int:id>', views.ProfileDelete, name="profile_delete"),

    path('billing', views.BillingView, name="billing"),
    path('update-billing/<int:id>', views.UpdateBillingView, name="updatebilling"),
    path('delete-billing/<int:id>', views.DeleteBillingView, name="deletebilling"),

]