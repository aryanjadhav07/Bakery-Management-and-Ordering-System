from django.urls import path
from . import views

urlpatterns = [
    path('customer-chat/', views.customer_chat_view, name='customer_chat'),
    path('baker-chat/', views.baker_chat_list, name='baker_chat_list'),
    path('chat/<int:user_id>/', views.baker_conversation_view, name='baker_conversation'),
    path('api/messages/<int:user_id>/', views.fetch_messages_api, name='api_fetch_messages'),
    path('api/send/', views.send_message_api, name='api_send_message'),
]
