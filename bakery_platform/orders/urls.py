from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('remove-from-cart/<str:item_key>/', views.remove_from_cart, name='remove_from_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('upload-receipt/<int:order_id>/', views.upload_receipt, name='upload_receipt'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('manage/', views.manage_orders, name='manage_orders'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
]
