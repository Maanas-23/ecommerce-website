from django.shortcuts import render, redirect
from .models import *
from user.views import *
import json
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.
def home(request):
    if is_vendor(request):
        return redirect("vendor-home")

    obj = Item.objects.all()
    items = []
    for i in obj:
        items.append(i)
    items.sort(key=lambda x: x.sales, reverse=True)

    print(i.sales for i in items)

    context = {
        'Item': items,
    }
    return render(request, 'home/home.html', context=context)


def cart(request):
    if not is_customer(request):
        return redirect('home')
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created2 = Cart.objects.get_or_create(customer=customer, complete=False)
        items = order.cartitem_set.all()
    else:
        items = list()
        order = dict()

    context = {
        'items': items, 'cart': order
    }
    return render(request, 'home/cart.html', context=context)


def update_cart(request):
    data = json.loads(request.body.decode())
    item_id, action = data['item'], data['action']
    user = request.user

    if action == 'remove-item':
        item = Item.objects.get(id=item_id)
        item.delete()
        return HttpResponse("deleted item")

    customer = Customer.objects.get(user=user)
    cart = Cart.objects.get(customer=customer)

    if action == 'add':
        item = Item.objects.get(id=item_id)
        cartitem = CartItem(item=item, cart=cart)
        l = cart.cartitem_set.all()
        for i in l:
            if i.item == item:
                i.qty += 1
                i.save()
                return redirect('addtocart')

        cartitem.save()
        return redirect('addtocart')

    elif action == 'append':
        i = CartItem.objects.get(id=item_id)
        i.qty += 1
        i.save()
        messages.success(request, 'Successfully added to cart')
        return HttpResponse("Already in cart, qty appended")

    elif action == 'remove':
        i = CartItem.objects.get(id=item_id)
        if i.qty > 1:
            i.qty -= 1
            i.save()
            return HttpResponse("Removed one qty of an item from cart")
        elif i.qty == 1:
            i.delete()
            return HttpResponse("Removed from cart")
        return HttpResponse("Not found in cart")

    elif action == 'buyall':
        if user.profile.balance >= cart.get_total_bill:
            user.profile.balance -= cart.get_total_bill
            user.profile.save()
            l = cart.cartitem_set.all()
            for i in l:
                item = i.item
                item.sales += i.qty
                order = Order.objects.get(vendor=item.vendor.vendor)
                orderitem = OrderItem(order=order, item=item, customer=user.customer, qty=i.qty, price=i.get_price())
                orderitem.save()
                item.save()
                prev_order_item = PrevOrderItem(item=item, qty=i.qty, price=i.get_price(), customer=user.customer)
                prev_order_item.save()
                i.delete()
            messages.success(request, "Successfully Bought all items")
            return HttpResponse("Bought")

        else:
            messages.warning(request, "Insufficient funds")
            return HttpResponse("Youre broke")

    elif action == "buy":
        cart_item = CartItem.objects.get(id=item_id)
        price = cart_item.get_total
        profile = Profile.objects.get_or_create(user=user, name=user.username)
        if user.profile.balance >= price:
            user.profile.balance -= price
            user.profile.save()
            item = cart_item.item
            item.sales += cart_item.qty
            order = Order.objects.get(vendor=item.vendor.vendor)
            orderitem = OrderItem(order=order, item=item, customer=user.customer, qty=cart_item.qty,
                                  price=cart_item.get_price())
            item.save()
            orderitem.save()
            prev_order_item = PrevOrderItem(item=item, qty=cart_item.qty, price=cart_item.get_price(),
                                            customer=user.customer)
            prev_order_item.save()
            cart_item.delete()
            messages.success(request, "Bought one item")
            return HttpResponse("Bought one item")
        else:
            messages.warning(request, "Insufficient funds")
            return HttpResponse("Youre broke")


def prev_orders(request):
    customer = request.user.customer
    items = customer.prevorderitem_set.all()
    return render(request, 'home/prev-orders.html', context={"Item": items})


# vendor stuff


def get_vendor_items(request):
    items = Item.objects.all()
    l = []
    for i in items:
        if i.vendor == request.user:
            l.append(i)
    return l


def vendor_home(request):
    if not is_vendor(request):
        return redirect('home')
    context = {
        'Item': get_vendor_items(request),
    }

    return render(request, 'home/vendor-home.html', context=context)


def orders(request):
    if not is_vendor(request):
        return redirect('home')
    order = Order.objects.get(vendor=request.user.vendor)
    items = order.orderitem_set.all()
    context = {"Item": items}

    return render(request, 'home/orders.html', context=context)


def manage_items(request):
    items = get_vendor_items(request)

    return render(request, 'home/orders.html', context={'Item': items})


def add_to_cart(request):
    messages.success(request, "Successfully added to cart")
    return redirect('login')
