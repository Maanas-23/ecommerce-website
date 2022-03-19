from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .forms import CustomerForm, ProfileForm, VendorForm, MoneyForm, AddItemForm
from django.contrib.auth import logout as auth_logout
from home.models import *
from django.http import HttpResponse
from .models import *


def is_customer(request):
    user = request.user
    if user.is_authenticated and user.groups.filter(name="vendor").exists() is False:
        return True
    return False


def is_vendor(request):
    user = request.user
    if user.is_authenticated and user.groups.filter(name="vendor").exists():
        return True
    return False


# name, gender, dob, address, balance
def vendor_signup(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            profile = Profile(user=user, name=profile_form.cleaned_data.get('name'),
                              dob=profile_form.cleaned_data.get('dob'),
                              address=profile_form.cleaned_data.get('address'),
                              gender=profile_form.cleaned_data.get('gender'))
            profile.save()

            vendor = Vendor(user=user)
            vendor.save()

            vendor_group = Group.objects.get(name="vendor")
            vendor_group.user_set.add(user)

            order = Order(vendor=vendor)
            order.save()

            messages.success(request, f'{username}, Your account has been created! You can log in to your account now')
            return redirect('vendor-login')

    else:
        form = CustomerForm()
        profile_form = ProfileForm()
    return render(request, 'user/vendor-signup.html', {'form': form, 'profile_form': profile_form})


# name, company_name, address, contact_no
def signup(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            profile = Profile(user=user, name=profile_form.cleaned_data.get('name'),
                              dob=profile_form.cleaned_data.get('dob'),
                              address=profile_form.cleaned_data.get('address'),
                              gender=profile_form.cleaned_data.get('gender'))
            profile.save()

            customer = Customer(user=user)
            customer.save()

            cart = Cart(customer=customer)
            cart.save()

            messages.success(request, f'{username}, Your account has been created! You can log in to your account now')
            return redirect('login')

    else:
        form = CustomerForm()
        profile_form = ProfileForm()
    return render(request, 'user/signup.html', {'form': form, 'profile_form': profile_form})


def logout(request):
    auth_logout(request)
    context = {
        'Item': Item.objects.all(),
    }
    messages.info(request, f'You have successfully logged out')
    return render(request, 'home/home.html', context=context)


def manage_funds(request):
    if not is_customer(request):
        return redirect('home')

    if request.method == 'POST':
        form = MoneyForm(request.POST)
        if form.is_valid():
            to_add, to_withdraw = form.cleaned_data.get('add'), form.cleaned_data.get('withdraw')
            user = request.user
            if to_add > 0:
                user.profile.balance += to_add
                user.profile.save()
                messages.success(request, f"Added Rs. {to_add} to account")
            elif to_withdraw > 0:
                user.profile.balance -= to_withdraw
                if user.profile.balance > 0:
                    user.profile.save()
                    messages.info(request, f"Withdrew Rs. {to_withdraw} from account")
                else:
                    messages.warning(request, "Insufficient funds, withdrawal failed")
            return redirect('home')
    else:
        form = MoneyForm()
    return render(request, 'user/manage-funds.html', {'form': form})


def add_item(request):
    if not is_vendor(request):
        return redirect('home')

    if request.method == 'POST':
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            item = Item(title=form.cleaned_data.get('title'), description=form.cleaned_data.get('description'),
                        price=form.cleaned_data.get('price'), discounted_price=form.cleaned_data.get('discounted_price')
                        , img=form.instance, vendor=request.user)

            item.save()

            return HttpResponse("worked")
    else:
        form = AddItemForm()
    return render(request, 'user/AddItemForm.html', {'form': form})
