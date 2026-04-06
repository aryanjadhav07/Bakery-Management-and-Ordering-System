from django.shortcuts import render, redirect
from .models import Course, Enrollment
from django.contrib.auth.decorators import login_required

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_detail(request, pk):
    course = Course.objects.get(pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})

@login_required
def enroll(request, pk):
    course = Course.objects.get(pk=pk)
    Enrollment.objects.create(user=request.user, course=course)
    return redirect('enrolled_courses')

from django.contrib import messages

@login_required
def enrolled_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'courses/enrolled_courses.html', {'enrollments': enrollments})

@login_required
def manage_courses(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'courses/manage_courses.html', {'courses': courses})

@login_required
def add_course(request):
    if not request.user.is_staff:
        return redirect('dashboard')
        
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price', 0.00)
        image = request.POST.get('image', '')
        
        Course.objects.create(
            title=title,
            description=description,
            price=price,
            image=image,
            created_by=request.user
        )
        messages.success(request, f'Course "{title}" added successfully!')
        return redirect('manage_courses')
        
    return render(request, 'courses/manage_courses.html')
