from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render,HttpResponse,redirect
from App_Lakshabay.forms import *
from App_Payment.forms import *
from App_Payment.models import *
from App_Order.models import *

def Dashboard(request):
    if request.user.is_superuser and request.user.is_authenticated:
        alluser=User.objects.all().exclude(is_superuser=True)
        orders=Order.objects.filter(ordered=True)
        items=Fitem.objects.all()
        booking=book.objects.all()
        context={
            'users':alluser,
            'orders':orders,
            'food_category':items,
            'bookings':booking,
        }
        return render(request,'App_Superadmin/index.html',context)
    else:
        return redirect('App_Superadmin:superadmin_login')
def Deleteuser(request,id):
    if request.user.is_superuser:
        if User.objects.filter(id=id).exists():
            us=User.objects.get(id=id)
            us.delete()
            messages.success(request,"User removed successfully",extra_tags="dashboard")
            return redirect('App_Superadmin:dashboard')
    else:
        return HttpResponse("<h1>You are not allow to delete any user</h1>")		
def SuperadminLogin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('App_Superadmin:dashboard')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            print(username,password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    return redirect('App_Superadmin:dashboard')
                else:
                    messages.info(request, "You are not a superuser",extra_tags="login")
                    return redirect('App_Superadmin:superadmin_login')
            else:
                messages.info(request, "Enter correct username and password",extra_tags="login")
                return redirect('App_Superadmin:superadmin_login')

        else:
            return render(request, 'App_Superadmin/login.html')



def SuperadminLogout(request):
    logout(request)
    return redirect('App_Superadmin:superadmin_login')

def Oderlist(request):
    orders = Order.objects.filter(ordered=True).order_by("-id")
    context = {
        'orders': orders,
    }
    return render(request, 'App_Superadmin/oderlist.html', context)


def ViewOrderDetails(request,id):
    if Order.objects.filter(id=id).exists():
        ord=Order.objects.get(id=id)
        context={
            'ord':ord,
        }
        return render(request,'App_Superadmin/order_details.html',context)
    else:
        return HttpResponse("<h1>Order is invalid</h1>")


def DeletereOrder(request, id):
    if request.user.is_superuser:
        if Order.objects.filter(id=id).exists():
            ord = Order.objects.get(id=id)
            ord.delete()
            messages.success(request, "Order removed successfully", extra_tags="deleteorder")
            return redirect('App_Superadmin:oderlist')
    else:
        return HttpResponse("<h1>You are not allow to delete any order</h1>")


def CategoryView(request):
    cat = category.objects.all()
    if request.method == "POST":
        cat = request.POST.get('cat_name')
        data = category.objects.create(
            category_name=cat
        )
        data.save()
        messages.success(request, 'Category succesfully added', extra_tags="cat_add")
        return redirect(request.POST['next'])
    context = {
        'catego': cat,
    }

    return render(request, 'App_Superadmin/categoryview.html', context)


def CatDeleteView(request, id):
    if category.objects.filter(category_id=id).exists():
        c = category.objects.get(category_id=id)
        if request.user.is_superuser:
            c.delete()
            messages.success(request, "Category succesfully deleted", extra_tags="cat_add")
            return redirect('App_Superadmin:category')
        else:
            return HttpResponse("<h1>You are not allow to delete it</h1>")
    else:
        return HttpResponse("<h1>Category not found</h1>")


def CatUpdateView(request, id):
    cat = category.objects.all()
    select_cat = category.objects.get(category_id=id)
    if request.method == "POST":
        cat_n = request.POST.get('cat_name')
        select_cat.category_name = cat_n
        select_cat.save()
        messages.success(request, 'Category succesfully updated', extra_tags="cat_add")
        return redirect('App_Superadmin:category')
    context = {
        'catego': cat,
        'select_cat': select_cat,
    }

    return render(request, 'App_Superadmin/updatecategoryview.html', context)

def MunuCategoryView(request):
    cat = menu_category.objects.all()
    if request.method == "POST":
        cat = request.POST.get('cat_name')
        data = menu_category.objects.create(
            menu_cat_name=cat
        )
        data.save()
        messages.success(request, 'Menu category succesfully added', extra_tags="menu_add")
        return redirect(request.POST['next'])
    context = {
        'catego': cat,
    }

    return render(request, 'App_Superadmin/menucategories.html', context)
def MenuCatUpdateView(request,id):
    cat = menu_category.objects.all()
    select_cat = menu_category.objects.get(menu_cat_id=id)
    if request.method == "POST":
        cat_n = request.POST.get('cat_name')
        select_cat.menu_cat_name = cat_n
        select_cat.save()
        messages.success(request, 'Menu category succesfully updated', extra_tags="menu_add")
        return redirect('App_Superadmin:menu-category')
    context = {
        'catego': cat,
        'select_cat': select_cat,
    }

    return render(request, 'App_Superadmin/updatemenucategoryview.html', context)
def MenuCatDeleteView(request,id):
    if menu_category.objects.filter(menu_cat_id=id).exists():
        c = menu_category.objects.get(menu_cat_id=id)
        if request.user.is_superuser:
            c.delete()
            messages.success(request, "Menu Category succesfully deleted", extra_tags="menu_add")
            return redirect('App_Superadmin:menu-category')
        else:
            return HttpResponse("<h1>You are not allow to delete it</h1>")
    else:
        return HttpResponse("<h1>Menu category not founded</h1>")


def FoodItem(request):
    fooditems=Fitem.objects.all().order_by("-item_id")
    menu_cat=menu_category.objects.all()
    if request.method=="POST":
        name=request.POST['item_name']
        des=request.POST['description']
        price=request.POST['item_price']

        cat=request.POST['category']
        print("cat id =",cat)
        if len(request.FILES) > 0:
            pho = request.FILES['item_photo']
            cate_name=menu_category.objects.get(menu_cat_id=cat)
            item=Fitem.objects.create(
                item_name=name,item_category=cate_name,item_description=des,item_price=price,photo=pho
            )
            item.save()
            messages.success(request,"Food Item Save succesfully",extra_tags="food_item")
            return redirect(request.POST['next'])
        else:
            cate_name = menu_category.objects.get(menu_cat_id=cat)
            item = Fitem.objects.create(
                item_name=name, item_category=cate_name, item_description=des, item_price=price
            )
            item.save()
            messages.success(request, "Food Item Save succesfully", extra_tags="food_item")
            return redirect(request.POST['next'])
    context={
        'food_items':fooditems,
        'menu_cat':menu_cat,

    }
    return render(request,'App_Superadmin/fooditems.html',context)

def FoodItemDeleteView(request,id):
    if Fitem.objects.filter(item_id=id).exists():
        c = Fitem.objects.get(item_id=id)
        if request.user.is_superuser:
            c.delete()
            messages.success(request, "Food Item succesfully deleted", extra_tags="food_item")
            return redirect('App_Superadmin:food_item')
        else:
            return HttpResponse("<h1>You are not allow to delete it</h1>")
    else:
        return HttpResponse("<h1>Menu category not founded</h1>")
def FoodItemUpdateView(request,id):
    fooditems = Fitem.objects.all().order_by("-item_id")
    menu_cat = menu_category.objects.all()
    my_item=Fitem.objects.get(item_id=id)
    if request.method == "POST":
        name = request.POST['item_name']
        des = request.POST['description']
        price = request.POST['item_price']

        cat = request.POST['category']
        pho=my_item.photo
        if len(request.FILES) > 0:
            pho = request.FILES['item_photo']
        cate_name = menu_category.objects.get(menu_cat_id=cat)
        my_item.item_name=name
        my_item.item_category=cate_name
        my_item.item_description=des
        my_item.item_price=price
        my_item.photo=pho
        my_item.save()
        messages.success(request, "Food Item update succesfully", extra_tags="food_item")
        return redirect('App_Superadmin:food_item')
    context = {
        'food_items': fooditems,
        'menu_cat': menu_cat,
        'my_item':my_item,

    }
    return render(request, 'App_Superadmin/fooditemupdate.html', context)


def GiftView(request):
    allgifts=gift.objects.all().order_by("-gift_id")
    cats=category.objects.all()
    if request.method=="POST":
        g_name=request.POST.get('gift_name')
        g_serial=request.POST.get('gift_serial')
        g_category=request.POST.get('gift_category')
        g_type=request.POST.get('gift_type')
        g_meta=request.POST.get('gift_meta')
        g_price=request.POST.get('gift_price')
        g_des=request.POST.get('gift_description')
        cat=category.objects.get(category_id=g_category)
        if len(request.FILES) !=0:
            g_photo = request.FILES['gift_images']
            gif=gift.objects.create(
                gift_name=g_name,gift_sl_no=g_serial,gift_category=cat,gift_type=g_type,gift_meta=g_meta,
                gift_price=g_price,gift_description=g_des,gift_image=g_photo
            )
            gif.save()
            messages.success(request, "Gift added succefully", extra_tags="gift")
            return redirect(request.POST['next'])
        else:
            messages.success(request,"Add image to save gift",extra_tags="gift")
            return redirect(request.POST['next'])
    context={
        'allgift':allgifts,
        'cats':cats,
    }
    return render(request,'App_Superadmin/giftspage.html',context)

def GiftUpdate(request,id):
    if gift.objects.filter(gift_id=id).exists():
        allgifts = gift.objects.all().order_by("-gift_id")
        cats = category.objects.all()
        select_gift=gift.objects.get(gift_id=id)
        if request.method == "POST":
            g_name = request.POST.get('gift_name')
            g_serial = request.POST.get('gift_serial')
            g_category = request.POST.get('gift_category')
            g_type = request.POST.get('gift_type')
            g_meta = request.POST.get('gift_meta')
            g_price = int(request.POST.get('gift_price'),2)
            g_des = request.POST.get('gift_description')
            cat = category.objects.get(category_id=g_category)
            g_photo=select_gift.gift_image
            if len(request.FILES) != 0:
                g_photo = request.FILES['gift_images']

            select_gift.gift_name=g_name
            select_gift.gift_sl_no=g_serial
            select_gift.gift_category=cat
            select_gift.gift_type=g_type
            select_gift.gift_meta=g_meta
            select_gift.gift_price=g_price
            select_gift.gift_description=g_des
            select_gift.gift_image=g_photo
            select_gift.save()
            messages.success(request, "Gift updated succefully", extra_tags="gift")
            return redirect(request.POST['next'])

        context = {
            'allgift': allgifts,
            'cats': cats,
            'select_gift':select_gift,
        }
        return render(request, 'App_Superadmin/giftupdatepage.html', context)
    else:
        return HttpResponse("<h1>Gift is not available</h1>")


def GiftDelete(request,id):
    if gift.objects.filter(gift_id=id).exists():
        c = gift.objects.get(gift_id=id)
        if request.user.is_superuser:
            c.delete()
            messages.success(request, "Gift succesfully deleted", extra_tags="gift")
            return redirect('App_Superadmin:gift')
        else:
            return HttpResponse("<h1>You are not allow to delete it</h1>")
    else:
        return HttpResponse("<h1>Gift not founded</h1>")
def Gallaryview(request):
    allgallary=gallery.objects.all()
    if request.method=="POST":
        name=request.POST.get('gallary_name')
        photo=request.FILES['gallary_photo']
        glr=gallery.objects.create(
            gallery_name=name,image=photo
        )
        glr.save()
        messages.success(request,"Image added to gallary",extra_tags="gallary")
        return redirect(request.POST['next'])
    context={
        'gallary':allgallary,
    }
    return render(request,'App_Superadmin/gallaryviewpage.html',context)

def GallaryUpdate(request,id):
    if gallery.objects.filter(gallery_id=id).exists():
        my_pho=gallery.objects.get(gallery_id=id)
        allgallary=gallery.objects.all()
        if request.method=="POST":
            name=request.POST.get('gallary_name')
            photo=my_pho.image
            if len(request.FILES)!=0:
                photo = request.FILES['gallary_photo']

            my_pho.gallery_name=name
            my_pho.image=photo
            my_pho.save()
            messages.success(request,"Image Updated successfully",extra_tags="gallary")
            return redirect(request.POST['next'])
        context={
            'gallary':allgallary,
            'my_photo':my_pho,
        }
        return render(request,'App_Superadmin/gallaryupdatepage.html',context)
    else:
        return HttpResponse("<h1>Gallary photo id is invalid</h1>")
def GallarytDelete(request,id):
    if gallery.objects.filter(gallery_id=id).exists():
        c = gallery.objects.get(gallery_id=id)
        if request.user.is_superuser:
            c.delete()
            messages.success(request, "Gallery succesfully deleted", extra_tags="gallary")
            return redirect('App_Superadmin:gallary')
        else:
            return HttpResponse("<h1>You are not allow to delete it</h1>")
    else:
        return HttpResponse("<h1>Gallery not founded</h1>")


def Bookingview(request):
    bookings = book.objects.all()
    context = {
        'bookings': bookings,
    }
    return render(request, 'App_Superadmin/bookingview.html', context)


def BookingDelete(request, id):
    if book.objects.filter(book_id=id).exists():
        c = book.objects.get(book_id=id)
        if request.user.is_superuser:
            c.delete()
            messages.success(request, "Booking succesfully deleted", extra_tags="book")
            return redirect('App_Superadmin:booking')
        else:
            return HttpResponse("<h1>You are not allow to delete it</h1>")
    else:
        return HttpResponse("<h1>Booking not founded</h1>")


def BookingUpdate(request, id):
    if book.objects.filter(book_id=id).exists():
        bookings = book.objects.all()
        my_booking = book.objects.get(book_id=id)
        if request.method == "POST":
            form = bookForm(request.POST, instance=my_booking)
            if form.is_valid():
                form.save()
                messages.success(request, "Booking updated succefully", extra_tags="book")
                return redirect('App_Superadmin:booking')
        else:
            form = bookForm(instance=my_booking)
        context = {
            'bookings': bookings,
            'book_form': form,
        }
        return render(request, 'App_Superadmin/bookingupdatepage.html', context)
    else:
        return HttpResponse("<h1>Booking is not available</h1>")


def BillingView(request):
    billing = BillingAddress.objects.all().order_by("-id")
    context = {
        'billings': billing,
    }
    return render(request, 'App_Superadmin/billingaddress.html', context)


def ProfileView(request):
    alluser = User.objects.all()

    context = {
        'allprofiles': alluser,
    }
    return render(request, 'App_Superadmin/profileview.html', context)





def ProfileDelete(request, id):
    if request.user.is_superuser:
        if User.objects.filter(id=id).exists():
            us = User.objects.get(id=id)
            us.delete()
            messages.success(request, "User removed successfully", extra_tags="profile")
            return redirect('App_Superadmin:profile')
        else:
            messages.success(request, "User is not matched", extra_tags="profile")
            return redirect('App_Superadmin:profile')

    else:
        return HttpResponse("<h1>You are not allow to delete any profile</h1>")



def UpdateBillingView(request,id):
    if BillingAddress.objects.filter(id=id).exists():
        my_billing = BillingAddress.objects.get(id=id)
        if request.method=="POST":
            form=BillingForm(request.POST,instance=my_billing)
            if form.is_valid():
                form.save()
                messages.success(request,"Billing address saved successfully",extra_tags="bill")
                return redirect('App_Superadmin:billing')
        else:
            form=form=BillingForm(instance=my_billing)
        context = {
            'bill_form': form,
        }
        return render(request,'App_Superadmin/billingupdatepage.html',context)
    else:
        return HttpResponse("<h1>Billing address not found</h1>")


def DeleteBillingView(request,id):
    if BillingAddress.objects.filter(id=id).exists():
        c = BillingAddress.objects.get(id=id)
        if request.user.is_superuser:
            c.delete()
            messages.success(request, "Billing Address succesfully deleted", extra_tags="bill")
            return redirect('App_Superadmin:billing')
        else:
            return HttpResponse("<h1>You are not allow to delete it</h1>")
    else:
        return HttpResponse("<h1>Billing Address not founded</h1>")