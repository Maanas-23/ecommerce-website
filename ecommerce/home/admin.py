from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Item)
admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PrevOrderItem)
# superuser
# rootpassword
