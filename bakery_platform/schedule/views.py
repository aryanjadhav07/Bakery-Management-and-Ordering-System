from django.shortcuts import render, redirect
from .forms import ClassScheduleForm
from .models import ClassSchedule
from courses.models import Enrollment
from django.contrib.auth.decorators import login_required

@login_required
def schedule_class(request):
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule')
    else:
        form = ClassScheduleForm()
    return render(request, 'schedule/schedule_form.html', {'form': form})

@login_required
def schedule_view(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    course_ids = [enrollment.course.id for enrollment in enrollments]
    schedules = ClassSchedule.objects.filter(course_id__in=course_ids)
    return render(request, 'schedule/schedule.html', {'schedules': schedules})
