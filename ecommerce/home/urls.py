from django.urls import path
from . import views
from user import views as user_views
# from django.views.generic import RedirectView

urlpatterns = [
    path('', views.home, name='home'),
    # path('', RedirectView.as_view(url='home/', permanent=False)),
    path('cart/', views.cart, name='cart'),
    path('manage-funds/', user_views.manage_funds, name='manage-funds'),
    path('addtocart/', views.add_to_cart, name='addtocart'),
    path('prev-orders/', views.prev_orders, name='prev-orders'),

    path('vendor/', views.vendor_home, name='vendor-home'),
    path('vendor/orders', views.orders, name='orders'),
    path('vendor/additem', user_views.add_item, name='add_item'),
    path('vendor/manage', views.manage_items, name='manage_items'),
]