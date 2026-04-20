from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Order
from courses.models import Enrollment, Course

def customer_required(view_func):
    @login_required
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('baker_dashboard')
        return view_func(request, *args, **kwargs)
    return wrap

def baker_required(view_func):
    @login_required
    def wrap(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrap

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST.get('role', 'Customer')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'signup.html')
            
        is_staff = (role == 'Baker')
        user = User.objects.create_user(username=username, email=email, password=password, is_staff=is_staff)
        user.save()
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
        
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

from orders.models import Order
from courses.models import Enrollment, Course, CourseEnrollment

@customer_required
def dashboard(request):
    user_orders = Order.objects.filter(user=request.user)
    context = {
        'total_orders': user_orders.count(),
        'completed_orders': user_orders.filter(status='Completed').count(),
        'active_courses': CourseEnrollment.objects.filter(
            user=request.user,
            payment_status=CourseEnrollment.STATUS_APPROVED
        ).count(),
        'recent_orders': user_orders.order_by('-created_at')[:3]
    }
    return render(request, 'dashboard.html', context)

@baker_required
def baker_dashboard(request):
    from chat.models import ChatMessage
    from courses.models import CourseEnrollment

    unread_messages_count = ChatMessage.objects.filter(receiver=request.user, is_read=False).count()

    all_msgs = ChatMessage.objects.filter(receiver=request.user).select_related('sender').order_by('-timestamp')
    recent_messages = []
    seen_senders = set()
    for msg in all_msgs:
        if msg.sender not in seen_senders:
            recent_messages.append(msg)
            seen_senders.add(msg.sender)
            if len(recent_messages) >= 5:
                break

    context = {
        'total_orders': Order.objects.filter(baker=request.user).count(),
        'pending_orders': Order.objects.filter(baker=request.user, status='Pending').count(),
        'total_courses': Course.objects.filter(created_by=request.user).count(),
        'unread_messages_count': unread_messages_count,
        'recent_messages': recent_messages,
        'pending_course_payments': CourseEnrollment.objects.filter(
            payment_status=CourseEnrollment.STATUS_PENDING
        ).count(),
    }
    return render(request, 'users/baker_dashboard.html', context)

@customer_required
def profile(request):
    return render(request, 'users/profile.html')

@customer_required
def select_baker(request):
    if request.method == 'POST':
        baker_id = request.POST.get('baker_id')
        next_url = request.POST.get('next', 'dashboard')
        if baker_id:
            request.session['selected_baker_id'] = int(baker_id)
            # Find baker name for message
            bkr = User.objects.filter(id=baker_id).first()
            name = bkr.username if bkr else "Baker"
            messages.success(request, f'Selected {name} as your Baker.')
            # If next_url is /select-baker/ or empty, fallback
            if next_url == '/users/select-baker/' or not next_url:
                next_url = 'dashboard'
            return redirect(next_url)
    
    bakers = User.objects.filter(is_staff=True)
    next_url = request.GET.get('next', 'dashboard')
    return render(request, 'users/select_baker.html', {'bakers': bakers, 'next_url': next_url})

