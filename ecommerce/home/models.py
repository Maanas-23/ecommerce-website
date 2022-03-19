from django.db import models
from django.contrib.auth.models import User
from user.models import Profile


# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    discounted_price = models.FloatField(null=True, blank=True)
    sales = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    # Foreign Key
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    img = models.ImageField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Items'

    def cartadd(self):
        item_to_add = CartItem(item=self, cart=Cart.objects.get(customer=User.customer))
        item_to_add.save()

    def get_img(self):
        return f'static/images/{self.img}'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    balance = models.FloatField(default=0)

    def __str__(self):
        return self.user.username


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    date_of_order = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.customer.user.username)

    @property
    def get_total_bill(self):
        items = self.cartitem_set.all()

        count = 0
        for i in items:
            count += i.get_total
        return count

    def get_total_items(self):
        k = len(self.cartitem_set.all())
        return k


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    @property
    def get_total(self):
        return self.get_price() * self.qty

    def get_price(self):
        if self.item.discounted_price:
            return self.item.discounted_price
        else:
            return self.item.price

    def get_title(self):
        return self.item.title

    def __str__(self):
        return str(self.item.title+' + '+self.cart.customer.user.username)


class PrevOrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now=True)
    price = models.FloatField(default=0)

    @property
    def get_total(self):
        return self.price * self.qty

    def get_title(self):
        return self.item.title

    def __str__(self):
        return str(self.item.title)


# Vendor models


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)


class Order(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vendor.user.username

    @property
    def get_total_sales(self):
        items = self.orderitem_set.all()

        count = 0
        for i in items:
            count += i.get_total
        return count

    def get_total_items_sold(self):
        k = len(self.orderitem_set.all())
        return k


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.FloatField(default=1000)
    date_sold = models.DateTimeField(auto_now_add=True)

    def get_customer(self):
        return self.customer.user.profile.name

    def get_price(self):
        return self.price

    def get_total(self):
        return self.price*self.qty
