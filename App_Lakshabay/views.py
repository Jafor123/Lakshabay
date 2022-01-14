from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from App_Lakshabay.forms import bookForm, ContactForm
from App_Lakshabay.models import *
from App_Order.models import *

def get_temp_user(request):
    users = TempCart.objects.all()
    if len(users) > 0:
        get_id = users.last()
        get_id = get_id.id
        print("last user id =", get_id)
    else:
        get_id = 0
        print("new", get_id)
    if "user_id" not in request.session:
        request.session["user_id"] = int(get_id) + 1

def getcart(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, purchased=False)
    else:
        carts = TempCart.objects.filter(user_id=request.session['user_id'], purchased=False)
    return carts
def getorder(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, ordered=False)
        if len(orders) != 0:
            order = orders[0]
        else:
            order = []
    else:
        orders = TempOrder.objects.filter(user_id=request.session['user_id'], ordered=False)
        if len(orders) != 0:
            order = orders[0]
        else:
            order = []
    return order

def index(request):
    get_temp_user(request)
    menu_cat = menu_category.objects.all()
    itm = Fitem.objects.all()
    gallery_photo=gallery.objects.all().order_by("-gallery_id")
    context = {
        'carts': getcart(request),
        'order': getorder(request),
        'menu_cat': menu_cat,
        'itm': itm,
        'gallery':gallery_photo,
    }
    return render(request,'App_Lakshabay/index.html',context)


def MenuView(request):
    menu_cat = menu_category.objects.all()
    itm = Fitem.objects.all()

    context = {
        'carts': getcart(request),
        'order': getorder(request),
        'menu_cat': menu_cat,
        'itm': itm,
    }
    return render(request,'App_Lakshabay/menu.html',context)

def onlineorder(request):
    menu_cat = menu_category.objects.all()
    itm = Fitem.objects.all()
    context = {
        'carts': getcart(request),
        'order': getorder(request),
        'menu_cat': menu_cat,
        'itm': itm,
    }
    return render(request,'App_Lakshabay/onlineorder.html',context)



def GiftView(request):
    cats=category.objects.all()
    gif=gift.objects.all()
    context = {
        'carts': getcart(request),
        'order': getorder(request),
        'gifts': gif,
        'cats': cats,
    }
    return render(request, 'App_Lakshabay/gift.html', context)

def Bookview(request):
    new_form = bookForm()
    if request.method == 'POST':
        new_form = bookForm(request.POST)
        if new_form.is_valid():
            new_form.save()
            messages.success(request, 'Your booking is listed', extra_tags="book")
            return redirect('App_Lakshabay:book')


    context = {
        'carts': getcart(request),
        'order': getorder(request),
        'bookForm': new_form,
    }
    return render(request, 'App_Lakshabay/booktable.html', context)

def ContactusView(request):
    if request.method=="POST":
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
            message = render_to_string('App_Lakshabay/message.html', {
                'email': form.cleaned_data.get('email'),
                'name': form.cleaned_data.get('name'),
                'pho': form.cleaned_data.get('phone'),
                'subject': "contact us",
                'message': form.cleaned_data.get('message'),
            })
            email = EmailMessage(
                "Message received confirmation", message, to=[settings.EMAIL_HOST_USER, ]
            )
            email.send()
            messages.success(request, 'We received your request, We will contact you soon.', extra_tags="book")
            return redirect('App_Lakshabay:contactus')
    else:
        form=ContactForm()
    context={
        'form':form,
        'carts': getcart(request),
        'order': getorder(request),
    }
    return render(request, 'App_Lakshabay/contact.html',context)


def GalleryView(request):
    images=gallery.objects.all()
    context = {
        'carts': getcart(request),
        'order': getorder(request),
        'gallery': images,
    }
    return render(request, 'App_Lakshabay/gallery.html', context)