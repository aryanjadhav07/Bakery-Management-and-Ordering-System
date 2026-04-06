from django.shortcuts import render, redirect, get_object_or_404
from .forms import ChatMessageForm
from .models import ChatMessage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
import json

def cleanup_and_mark_messages(queryset):
    now = timezone.now()
    cutoff = now - timedelta(hours=24)
    # Clean up old
    ChatMessage.objects.filter(is_active=True, viewed_at__lt=cutoff).update(is_active=False)
    # Mark viewed for anything returned in queryset
    queryset.filter(viewed_at__isnull=True).update(viewed_at=now)

@login_required
def customer_chat_view(request):
    if request.user.is_staff:
        return redirect('baker_chat_list')

    selected_baker_id = request.session.get('selected_baker_id')
    if not selected_baker_id:
        return redirect('/users/select-baker/?next=/chat/customer-chat/')
        
    baker = get_object_or_404(User, id=selected_baker_id)
        
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = baker
            message.baker = baker
            message.save()
            return redirect('customer_chat')
    else:
        form = ChatMessageForm()
        
    base_qs = ChatMessage.objects.filter(
        baker=baker,
        sender__in=[request.user, baker],
        receiver__in=[request.user, baker],
        is_active=True
    )
    cleanup_and_mark_messages(base_qs)
    
    messages = base_qs.order_by('timestamp')
    return render(request, 'chat/chat.html', {'form': form, 'chat_messages': messages, 'baker': baker})

@login_required
def baker_chat_list(request):
    from django.urls import reverse
    if not request.user.is_staff:
        return redirect('customer_chat')
        
    cleanup_and_mark_messages(ChatMessage.objects.none()) # Just trigger cleanup
    
    all_msgs = ChatMessage.objects.filter(baker=request.user, is_active=True).select_related('sender', 'receiver').order_by('-timestamp')
    
    conversations = []
    seen_users = set()
    for msg in all_msgs:
        other_user = msg.sender if msg.receiver == request.user else msg.receiver
        if other_user not in seen_users:
            conversations.append({
                'user': other_user,
                'message': msg.message,
                'timestamp': msg.timestamp,
                'is_read': msg.is_read if msg.receiver == request.user else True
            })
            seen_users.add(other_user)
            
    active_user_id = request.GET.get('user_id')
    active_customer = None
    if active_user_id:
        active_customer = get_object_or_404(User, id=active_user_id)
    elif conversations:
        active_customer = conversations[0]['user']
            
    return render(request, 'chat/baker_chat.html', {
        'conversations': conversations,
        'active_customer': active_customer
    })

@login_required
def baker_conversation_view(request, user_id):
    from django.urls import reverse
    if not request.user.is_staff:
        return redirect('customer_chat')
    url = reverse('baker_chat_list')
    return redirect(f'{url}?user_id={user_id}')

@login_required
def fetch_messages_api(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    # Mark as read
    ChatMessage.objects.filter(sender=other_user, receiver=request.user, is_read=False, is_active=True).update(is_read=True)

    # Determine baker filter
    req_baker = request.user if request.user.is_staff else other_user

    base_qs = ChatMessage.objects.filter(
        baker=req_baker,
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user],
        is_active=True
    )
    cleanup_and_mark_messages(base_qs)
    
    messages = base_qs.order_by('timestamp')
    
    msg_list = []
    for m in messages:
        msg_list.append({
            'id': m.id,
            'sender_id': m.sender.id,
            'sender_username': m.sender.username,
            'message': m.message,
            'timestamp': m.timestamp.strftime('%H:%M')
        })
        
    return JsonResponse({'messages': msg_list})

@login_required
@require_POST
def send_message_api(request):
    try:
        data = json.loads(request.body)
        receiver_id = data.get('receiver_id')
        message_text = data.get('message', '').strip()
        
        if not receiver_id or not message_text:
            return JsonResponse({'error': 'Invalid data'}, status=400)
            
        receiver = get_object_or_404(User, id=receiver_id)
        
        # Determine baker context
        baker = request.user if request.user.is_staff else receiver
        
        msg = ChatMessage.objects.create(
            sender=request.user,
            receiver=receiver,
            baker=baker,
            message=message_text,
            is_read=False
        )
        # Trigger cleanup logic just to be thorough on creation
        cleanup_and_mark_messages(ChatMessage.objects.none())
        
        return JsonResponse({
            'status': 'success',
            'message': {
                'id': msg.id,
                'sender_id': msg.sender.id,
                'sender_username': msg.sender.username,
                'message': msg.message,
                'timestamp': msg.timestamp.strftime('%H:%M')
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
