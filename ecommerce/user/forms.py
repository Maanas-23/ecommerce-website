from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, ManageFunds, ItemForm


# Forms for a customer login
class CustomerForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'dob', 'address', 'gender']


class VendorForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MoneyForm(forms.ModelForm):
    class Meta:
        model = ManageFunds
        fields = ['add', 'withdraw']


class AddItemForm(forms.ModelForm):
    class Meta:
        model = ItemForm
        fields = ['title', 'description', 'price', 'discounted_price', 'img']
