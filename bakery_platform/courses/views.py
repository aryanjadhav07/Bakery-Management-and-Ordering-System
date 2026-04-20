from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Course, CourseEnrollment


# ─────────────────────────────────────────────────────────────────
# CUSTOMER VIEWS
# ─────────────────────────────────────────────────────────────────

@login_required
def course_list(request):
    courses = Course.objects.all().order_by('-created_at')

    # Build a dict: course_id → enrollment (or None)
    enrollment_map = {
        e.course_id: e
        for e in CourseEnrollment.objects.filter(user=request.user)
    }

    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'enrollment_map': enrollment_map,
    })


@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    enrollment = CourseEnrollment.objects.filter(
        user=request.user, course=course
    ).first()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'enrollment': enrollment,
    })


@login_required
def enroll(request, pk):
    """
    Step 1 → redirect to payment page.
    Creates a Pending enrollment record so the payment page has an ID to work with.
    """
    if request.user.is_staff:
        messages.error(request, 'Bakers cannot enroll in courses.')
        return redirect('courses')

    course = get_object_or_404(Course, pk=pk)

    # If already enrolled (any status), go to payment / status page
    enrollment, created = CourseEnrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'amount': course.price, 'payment_status': CourseEnrollment.STATUS_PENDING},
    )

    if not created and enrollment.is_approved:
        messages.info(request, 'You are already enrolled in this course.')
        return redirect('enrolled_courses')

    return redirect('course_payment', pk=course.pk)


@login_required
def course_payment(request, pk):
    """Step 2 — show payment page with receipt upload."""
    course = get_object_or_404(Course, pk=pk)
    enrollment = get_object_or_404(
        CourseEnrollment, user=request.user, course=course
    )

    if enrollment.is_approved:
        messages.info(request, 'Your payment is already approved.')
        return redirect('enrolled_courses')

    if request.method == 'POST':
        if 'receipt_image' not in request.FILES:
            messages.error(request, 'Please select a receipt image to upload.')
            return render(request, 'courses/course_payment.html', {
                'course': course,
                'enrollment': enrollment,
            })

        enrollment.receipt_image = request.FILES['receipt_image']
        enrollment.payment_status = CourseEnrollment.STATUS_PENDING
        enrollment.rejection_note = None
        enrollment.amount = course.price
        enrollment.save()

        messages.success(
            request,
            'Receipt uploaded! Your payment is pending baker verification.'
        )
        return redirect('enrolled_courses')

    return render(request, 'courses/course_payment.html', {
        'course': course,
        'enrollment': enrollment,
    })


@login_required
def enrolled_courses(request):
    enrollments = (
        CourseEnrollment.objects
        .filter(user=request.user)
        .select_related('course', 'course__created_by')
        .order_by('-created_at')
    )
    return render(request, 'courses/enrolled_courses.html', {
        'enrollments': enrollments,
    })


# ─────────────────────────────────────────────────────────────────
# BAKER VIEWS
# ─────────────────────────────────────────────────────────────────

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
        title       = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        price       = request.POST.get('price', '0.00')
        image       = request.POST.get('image', '').strip()
        video_url   = request.POST.get('video_url', '').strip()

        if not title or not description:
            messages.error(request, 'Title and description are required.')
            return redirect('manage_courses')

        Course.objects.create(
            title=title,
            description=description,
            price=price,
            image=image or None,
            video_url=video_url or None,
            created_by=request.user,
        )
        messages.success(request, f'Course "{title}" added successfully!')
        return redirect('manage_courses')

    return redirect('manage_courses')


@login_required
def manage_course_payments(request):
    """Baker sees all pending/processed course payment requests."""
    if not request.user.is_staff:
        return redirect('dashboard')

    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment_id')
        action        = request.POST.get('action')
        enrollment    = get_object_or_404(CourseEnrollment, pk=enrollment_id)

        if action == 'approve':
            enrollment.payment_status = CourseEnrollment.STATUS_APPROVED
            enrollment.approved_at    = timezone.now()
            enrollment.rejection_note = None
            enrollment.save()
            messages.success(
                request,
                f'Payment approved for {enrollment.user.username} — {enrollment.course.title}.'
            )
        elif action == 'reject':
            note = request.POST.get('rejection_note', '').strip()
            enrollment.payment_status = CourseEnrollment.STATUS_REJECTED
            enrollment.rejection_note = note or 'Payment rejected by baker.'
            enrollment.approved_at    = None
            enrollment.save()
            messages.warning(
                request,
                f'Payment rejected for {enrollment.user.username}.'
            )

        return redirect('manage_course_payments')

    # Show pending first, then others
    enrollments = (
        CourseEnrollment.objects
        .select_related('user', 'course')
        .order_by(
            # Pending first
            models_order_pending(),
            '-created_at'
        )
    )
    pending_count = enrollments.filter(
        payment_status=CourseEnrollment.STATUS_PENDING
    ).count()

    return render(request, 'courses/manage_course_payments.html', {
        'enrollments': enrollments,
        'pending_count': pending_count,
    })


def models_order_pending():
    """Helper: returns a Case expression to sort Pending first."""
    from django.db.models import Case, When, Value, IntegerField
    return Case(
        When(payment_status=CourseEnrollment.STATUS_PENDING, then=Value(0)),
        When(payment_status=CourseEnrollment.STATUS_REJECTED, then=Value(1)),
        When(payment_status=CourseEnrollment.STATUS_APPROVED, then=Value(2)),
        default=Value(3),
        output_field=IntegerField(),
    )
