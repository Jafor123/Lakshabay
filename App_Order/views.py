from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from App_Order.models import *
from App_Lakshabay.models import *
from django.contrib import messages
from App_Lakshabay import views as v

def item_add_to_cart(request,pk):
    if request.user.is_authenticated:
        item = get_object_or_404(Fitem, pk=pk)
        print("Item")
        print(item)
        order_item = Cart.objects.get_or_create(item2=item,user=request.user,purchased=False)
        print("Order Item Object:")
        print(order_item)
        print(order_item[0])
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        print("Order Qs:")
        print(order_qs)
        #print(order_qs[0])
        if order_qs.exists():
            order = order_qs[0]
            print("If Order exist")
            print(order)
            if order.orderitems.filter(item2=item).exists():
                order_item[0].quantity += 1
                order_item[0].save()
                messages.info(request, "This item quantity was updated.")
                return redirect("App_Lakshabay:onlineorder")
            else:
                order.orderitems.add(order_item[0])
                messages.info(request, "This item was added to your cart.")
                return redirect("App_Lakshabay:onlineorder")
        else:
            order = Order(user=request.user)
            order.save()
            order.orderitems.add(order_item[0])
            messages.info(request, "This item was added to your cart.")
            return redirect("App_Lakshabay:onlineorder")
    else:
        item = get_object_or_404(Fitem, pk=pk)
        print("Item")
        print(item)
        order_item = TempCart.objects.get_or_create(item2=item, user_id=request.session["user_id"], purchased=False)
        print("Order Item Object:")
        print(order_item)
        print(order_item[0])
        order_qs = TempOrder.objects.filter(user_id=request.session["user_id"], ordered=False)
        print("Order Qs:")
        print(order_qs)
        # print(order_qs[0])
        if order_qs.exists():
            order = order_qs[0]
            print("If Order exist")
            print(order)
            if order.orderitems.filter(item2=item).exists():
                order_item[0].quantity += 1
                order_item[0].save()
                messages.info(request, "This item quantity was updated.")
                return redirect("App_Lakshabay:onlineorder")
            else:
                order.orderitems.add(order_item[0])
                messages.info(request, "This item was added to your cart.")
                return redirect("App_Lakshabay:onlineorder")
        else:
            order = TempOrder(user_id=request.session["user_id"])
            order.save()
            order.orderitems.add(order_item[0])
            messages.info(request, "This item was added to your cart.")
            return redirect("App_Lakshabay:onlineorder")

def add_to_cart(request, pk):
    if request.user.is_authenticated:
        item = get_object_or_404(gift, pk=pk)
        print("Item")
        print(item)
        order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False,item2=None)
        print("Order Item Object:")
        print(order_item)
        print(order_item[0])
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        print("Order Qs:")
        print(order_qs)
        #print(order_qs[0])
        if order_qs.exists():
            order = order_qs[0]
            print("If Order exist")
            print(order)
            if order.orderitems.filter(item=item).exists():
                order_item[0].quantity += 1
                order_item[0].save()
                messages.info(request, "This item quantity was updated.")
                return redirect("App_Lakshabay:gifts")
            else:
                order.orderitems.add(order_item[0])
                messages.info(request, "This item was added to your cart.")
                return redirect("App_Lakshabay:gifts")
        else:
            order = Order(user=request.user)
            order.save()
            order.orderitems.add(order_item[0])
            messages.info(request, "This item was added to your cart.")
            return redirect("App_Lakshabay:gifts")
    else:
        item = get_object_or_404(gift, pk=pk)
        print("Item")
        print(item)
        order_item = TempCart.objects.get_or_create(item=item, user_id=request.session["user_id"], purchased=False,item2_id=None)
        print("Order Item Object:")
        print(order_item)
        print(order_item[0])
        order_qs = TempOrder.objects.filter(user_id=request.session["user_id"], ordered=False)
        print("Order Qs:")
        print(order_qs)
        # print(order_qs[0])
        if order_qs.exists():
            order = order_qs[0]
            print("If Order exist")
            print(order)
            if order.orderitems.filter(item=item).exists():
                order_item[0].quantity += 1
                order_item[0].save()
                messages.info(request, "This item quantity was updated.")
                return redirect("App_Lakshabay:gifts")
            else:
                order.orderitems.add(order_item[0])
                messages.info(request, "This item was added to your cart.")
                return redirect("App_Lakshabay:gifts")
        else:
            order = TempOrder(user_id=request.session["user_id"])
            order.save()
            order.orderitems.add(order_item[0])
            messages.info(request, "This item was added to your cart.")
            return redirect("App_Lakshabay:gifts")


def item_cart_view(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, purchased=False,item=None)
        orders = Order.objects.filter(user=request.user, ordered=False)
        if carts.exists() and orders.exists():
            order = orders[0]
            return render(request, 'App_Order/item_cart.html', context={'carts':carts, 'order':order})
        else:
            messages.warning(request, "You don't have any item in your cart!")
            return redirect("App_Lakshabay:onlineorder")
    else:
        carts = TempCart.objects.filter(user_id=request.session['user_id'], purchased=False,item=None)
        orders = TempOrder.objects.filter(user_id=request.session['user_id'], ordered=False)
        if carts.exists() and orders.exists():
            order = orders[0]
            return render(request, 'App_Order/item_cart.html', context={'carts': carts, 'order': order})
        else:
            messages.warning(request, "You don't have any item in your cart!")
            return redirect("App_Lakshabay:onlineorder")

def cart_view(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, purchased=False)
        orders = Order.objects.filter(user=request.user, ordered=False)
        print("shw=",carts)
        if carts.exists() and orders.exists():
            order = orders[0]
            return render(request, 'App_Order/cart.html', context={'carts':carts, 'order':order})
        else:
            messages.warning(request, "You don't have any item in your cart!")
            return redirect("App_Lakshabay:gifts")
    else:
        carts = TempCart.objects.filter(user_id=request.session['user_id'], purchased=False)
        orders = TempOrder.objects.filter(user_id=request.session['user_id'], ordered=False)

        if carts.exists() and orders.exists():
            order = orders[0]
            return render(request, 'App_Order/cart.html', context={'carts': carts, 'order': order})
        else:
            messages.warning(request, "You don't have any item in your cart!")
            return redirect("App_Lakshabay:gifts")


def remove_from_cart(request, pk):
    item = get_object_or_404(gift, pk=pk)
    if request.user.is_authenticated:
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, "This item was removed form your cart")
                return redirect("App_Order:cart")
            else:
                messages.info(request, "This item was not in your cart.")
                return redirect("App_Lakshabay:gifts")
        else:
            messages.info(request, "You don't have an active order")
            return redirect("App_Lakshabay:gifts")
    else:
        order_qs = TempOrder.objects.filter(user_id=request.session['user_id'], ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = TempCart.objects.filter(item=item, user_id=request.session['user_id'], purchased=False)[0]
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, "This item was removed form your cart")
                return redirect("App_Order:cart")
            else:
                messages.info(request, "This item was not in your cart.")
                return redirect("App_Lakshabay:gifts")
        else:
            messages.info(request, "You don't have an active order")
            return redirect("App_Lakshabay:gifts")


def increase_cart(request, pk):
    item = get_object_or_404(gift, pk=pk)
    if request.user.is_authenticated:
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                if order_item.quantity >= 1:
                    order_item.quantity += 1
                    order_item.save()
                    messages.info(request, f"{item.gift_name} quantity has been updated",extra_tags="cart")
                    return redirect("App_Order:cart")
            else:
                messages.info(request, f"{item.gift_name} is not in your cart",extra_tags="cart")
                return redirect("App_Lakshabay:gifts")
        else:
            messages.info(request, "You don't have an active order",extra_tags="cart")
            return redirect("App_Lakshabay:gifts")
    else:
        order_qs = TempOrder.objects.filter(user_id=request.session['user_id'], ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = TempCart.objects.filter(item=item, user_id=request.session['user_id'], purchased=False)[0]
                if order_item.quantity >= 1:
                    order_item.quantity += 1
                    order_item.save()
                    messages.info(request, f"{item.gift_name} quantity has been updated",extra_tags="cart")
                    return redirect("App_Order:cart")
            else:
                messages.info(request, f"{item.gift_name} is not in your cart",extra_tags="cart")
                return redirect("App_Lakshabay:gifts")
        else:
            messages.info(request, "You don't have an active order",extra_tags="cart")
            return redirect("App_Lakshabay:gifts")


def decrease_cart(request, pk):
    item = get_object_or_404(gift, pk=pk)
    if request.user.is_authenticated:
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.info(request, f"{item.gift_name} quantity has been updated",extra_tags="cart")
                    return redirect("App_Order:cart")
                else:
                    order.orderitems.remove(order_item)
                    order_item.delete()
                    messages.warning(request, f"{item.gift_name} item has been removed from your cart",extra_tags="cart")
                    return redirect("App_Order:cart")
            else:
                messages.info(request, f"{item.gift_name} is not in your cart",extra_tags="cart")
                return redirect("App_Lakshabay:gifts")
        else:
            messages.info(request, "You don't have an active order",extra_tags="cart")
            return redirect("App_Lakshabay:gifts")
    else:
        order_qs = TempOrder.objects.filter(user_id=request.session['user_id'], ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = TempCart.objects.filter(item=item, user_id=request.session['user_id'], purchased=False)[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.info(request, f"{item.gift_name} quantity has been updated",extra_tags="cart")
                    return redirect("App_Order:cart")
                else:
                    order.orderitems.remove(order_item)
                    order_item.delete()
                    messages.warning(request, f"{item.gift_name} item has been removed from your cart",extra_tags="cart")
                    return redirect("App_Order:cart")
            else:
                messages.info(request, f"{item.name} is not in your cart",extra_tags="cart")
                return redirect("App_Lakshabay:gifts")
        else:
            messages.info(request, "You don't have an active order",extra_tags="cart")
            return redirect("App_Lakshabay:gifts")


def itemincrease_cart(request, pk):
    print("+")
    item = get_object_or_404(Fitem, pk=pk)
    if request.user.is_authenticated:
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item2=item).exists():
                order_item = Cart.objects.filter(item2=item, user=request.user, purchased=False)[0]
                if order_item.quantity >= 1:
                    order_item.quantity += 1
                    order_item.save()
                    messages.info(request, f"{item.item_name} quantity has been updated",extra_tags="cart")
                    return redirect("App_Order:cart")
            else:
                messages.info(request, f"{item.item_name} is not in your cart",extra_tags="cart")
                return redirect("App_Lakshabay:onlineorder")
        else:
            messages.info(request, "You don't have an active order",extra_tags="cart")
            return redirect("App_Lakshabay:onlineorder")
    else:
        order_qs = TempOrder.objects.filter(user_id=request.session['user_id'], ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item2=item).exists():
                order_item = TempCart.objects.filter(item2=item, user_id=request.session['user_id'], purchased=False)[0]
                if order_item.quantity >= 1:
                    order_item.quantity += 1
                    order_item.save()
                    messages.info(request, f"{item.item_name} quantity has been updated",extra_tags="cart")
                    return redirect("App_Order:cart")
            else:
                messages.info(request, f"{item.item_name} is not in your cart",extra_tags="cart")
                return redirect("App_Lakshabay:onlineorder")
        else:
            messages.info(request, "You don't have an active order",extra_tags="cart")
            return redirect("App_Lakshabay:onlineorder")




def itemdecrease_cart(request, pk):
    print("-")
    item = get_object_or_404(Fitem, pk=pk)
    if request.user.is_authenticated:
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item2=item).exists():
                order_item = Cart.objects.filter(item2=item, user=request.user, purchased=False)[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.info(request, f"{item.item_name} quantity has been updated",extra_tags="cart")
                    return redirect("App_Order:cart")
                else:
                    order.orderitems.remove(order_item)
                    order_item.delete()
                    messages.warning(request, f"{item.item_name} item has been removed from your cart",extra_tags="cart")
                    return redirect("App_Order:cart")
            else:
                messages.info(request, f"{item.item_name} is not in your cart",extra_tags="cart")
                return redirect("App_Lakshabay:onlineorder")
        else:
            messages.info(request, "You don't have an active order",extra_tags="cart")
            return redirect("App_Lakshabay:onlineorder")
    else:
        order_qs = TempOrder.objects.filter(user_id=request.session['user_id'], ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item2=item).exists():
                order_item = TempCart.objects.filter(item2=item, user_id=request.session['user_id'], purchased=False)[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.info(request, f"{item.item_name} quantity has been updated",extra_tags="cart")
                    return redirect("App_Order:cart")
                else:
                    order.orderitems.remove(order_item)
                    order_item.delete()
                    messages.warning(request, f"{item.item_name} item has been removed from your cart",extra_tags="cart")
                    return redirect("App_Order:cart")
            else:
                messages.info(request, f"{item.item_name} is not in your cart",extra_tags="cart")
                return redirect("App_Lakshabay:onlineorder")
        else:
            messages.info(request, "You don't have an active order",extra_tags="cart")
            return redirect("App_Lakshabay:onlineorder")


def itemremove_from_cart(request,pk):
    item = get_object_or_404(Fitem, pk=pk)
    if request.user.is_authenticated:
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item2=item).exists():
                order_item = Cart.objects.filter(item2=item, user=request.user, purchased=False)[0]
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, "This item was removed form your cart")
                return redirect("App_Order:cart")
            else:
                messages.info(request, "This item was not in your cart.")
                return redirect("App_Lakshabay:onlineorder")
        else:
            messages.info(request, "You don't have an active order")
            return redirect("App_Lakshabay:onlineorder")
    else:
        order_qs = TempOrder.objects.filter(user_id=request.session['user_id'], ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item2=item).exists():
                order_item = TempCart.objects.filter(item2=item, user_id=request.session['user_id'], purchased=False)[0]
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, "This item was removed form your cart")
                return redirect("App_Order:cart")
            else:
                messages.info(request, "This item was not in your cart.")
                return redirect("App_Lakshabay:onlineorder")
        else:
            messages.info(request, "You don't have an active order")
            return redirect("App_Lakshabay:onlineorder")
