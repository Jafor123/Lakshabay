from django.urls import path
from App_Payment import views

app_name = "App_Payment"
from App_Payment.views import (
    CreateCheckoutSessionView
)
urlpatterns = [
    path('checkout/', views.checkout, name="checkout"),
    path('payment/<int:id>',views.PaymentView,name='payment'),
    path('cancel/', views.CancelView, name='cancel'),
    path('success/', views.SuccessView, name='success'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),

]
