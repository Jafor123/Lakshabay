from decimal import Decimal
import socket

from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views import View
from App_Payment.forms import SignUpForm,BillingForm
from lakshabay import settings
from App_Lakshabay.models import *
from App_Order.models import *
from App_Lakshabay.views import getcart,getorder

stripe.api_key = settings.STRIPE_SECRET_KEY
def checkout(request):
    if request.user.is_authenticated:
        try:
            orders = Order.objects.filter(user=request.user, ordered=False).latest('id')
        except:
            orders=None
        print(orders.ordered)
        if request.method=="POST":
            f_name=request.POST.get('firstname')
            l_name=request.POST.get('lastname')
            c_name=request.POST.get('company')
            cn_name=request.POST.get('country')
            ad=request.POST.get('address_1')
            ad2=request.POST.get('address_2')
            city=request.POST.get('city')
            sate=request.POST.get('state')
            zip=request.POST.get('zipcode')
            ph=request.POST.get('phone')
            adi=request.POST.get('additional_info')

            billing=BillingAddress()
            billing.firstname=f_name
            billing.lastname=l_name
            billing.country=cn_name
            billing.company=c_name
            billing.address=ad
            billing.address2=ad2
            billing.city=city
            billing.state=sate
            billing.zipcode=zip
            billing.phone=ph
            billing.aditional_info=adi
            billing.save()
            orders.billing_address=billing
            orders.save()
            return redirect(orders.get_absolute_url())
        else:
            context = {
                'carts': getcart(request),
                'order': getorder(request),
                'orders_not_null':orders,
            }
            return render(request, 'App_Payment/checkout.html', context)
    else:
        if request.method=="POST":
            form=SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                my_order = TempCart.objects.filter(user_id=request.session['user_id'], purchased=False)
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                for i in my_order:
                    if i.item2 == None:
                        new_cart = Cart.objects.create(
                            user=request.user, item=i.item, quantity=i.quantity
                        )
                        new_cart.save()
                    else:
                        new_cart = Cart.objects.create(
                            user=request.user, item2=i.item2, quantity=i.quantity
                        )
                        new_cart.save()
                print("ordered")
                ord = Order.objects.create(
                    user=request.user, ordered=False
                )
                ord.save()
                ord = Order.objects.get(user=request.user, ordered=False)
                cart_list = Cart.objects.filter(user=request.user)
                for i in cart_list:
                    ord.orderitems.add(i)
                ord.save()
                for i in cart_list:
                    i.purchased = True
                    i.save()
                return redirect('App_Payment:checkout')
        else:
            form=SignUpForm()
        context = {
            'carts': getcart(request),
            'order': getorder(request),
            'stripe':settings.STRIPE_PUBLISHABLE_KEY,
            'form':form,
        }
        return render(request, 'App_Payment/checkout.html', context)


def PaymentView(request,id):
    msg=None
    if Order.objects.filter(id=id).exists():
        order=Order.objects.get(id=id)
    else:
        msg="Your Order id is invalid"
    context={
        'msg':msg,
        'orders':order,
        'carts': getcart(request),
        'order': getorder(request),
        'stripe': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request,'App_Payment/payment.html',context)


stripe.api_key = settings.STRIPE_SECRET_KEY
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        donate = Order.objects.get(id=product_id)
        title="Order ID :"+str(donate.id)
        YOUR_DOMAIN = "http://54.227.68.244:8777"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'gbp',
                        'unit_amount':int(donate.get_totals()*100),
                        'product_data': {
                            'name': title
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": 12
            },
            mode='payment',
            success_url=request.build_absolute_uri(
            reverse('App_Payment:success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('App_Payment:cancel')),
        )
        donate.paymentId = checkout_session['payment_intent']
        donate.save()

        return JsonResponse({
            'id': checkout_session.id
        })


def SuccessView(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
        return HttpResponseNotFound()
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    ord = get_object_or_404(Order, paymentId=session.payment_intent)
    ord.ordered=True
    ord.save()
    for i in ord.orderitems.all():
        i.purchased = True
        i.save()

    context = {
        'carts': getcart(request),
        'order': getorder(request),
    }
    return render(request,'App_Payment/success.html',context)



def CancelView(request):
    context = {
        'carts': getcart(request),
        'order': getorder(request),
    }
    return render(request,'App_Payment/cancel.html',context)

