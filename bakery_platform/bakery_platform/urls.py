"""
URL configuration for bakery_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views
from orders import views as order_views
from products import views as product_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('courses/', include('courses.urls')),
    path('chat/', include('chat.urls')),
    path('schedule/', include('schedule.urls')),
    path('ai-assistant/', include('ai_assistant.urls')),
    
    # Cart & Order routes
    path('cart/', order_views.view_cart, name='cart'),
    path('add-to-cart/<int:product_id>/', order_views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<str:item_key>/', order_views.remove_from_cart, name='remove_from_cart'),
    path('place-order/', order_views.place_order, name='place_order'),
    path('payment/<int:order_id>/', order_views.payment, name='payment'),
    path('upload-receipt/<int:order_id>/', order_views.upload_receipt, name='upload_receipt'),
    path('cancel-order/<int:order_id>/', order_views.cancel_order, name='cancel_order'),
    path('my-orders/', order_views.my_orders, name='my_orders'),

    # Baker Product routes
    path('add-product/', product_views.add_product, name='add_product'),
    path('edit-product/<int:id>/', product_views.edit_product, name='edit_product'),
    path('delete-product/<int:id>/', product_views.delete_product, name='delete_product'),
    path('manage-products/', product_views.manage_products, name='manage_products'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
