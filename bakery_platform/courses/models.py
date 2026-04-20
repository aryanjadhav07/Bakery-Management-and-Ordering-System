from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampedModel


class Course(TimestampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.URLField(blank=True, null=True)
    video_url = models.URLField(
        blank=True, null=True,
        help_text="YouTube or other video URL for this course"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='courses_taught', null=True, blank=True
    )

    def __str__(self):
        return self.title

    @property
    def is_youtube(self):
        if not self.video_url:
            return False
        return 'youtube.com' in self.video_url or 'youtu.be' in self.video_url


class CourseEnrollment(TimestampedModel):
    """
    Replaces the old Enrollment model.
    Tracks payment receipt upload and baker approval status.
    """
    STATUS_PENDING  = 'Pending'
    STATUS_APPROVED = 'Approved'
    STATUS_REJECTED = 'Rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING,  'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    user   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    receipt_image = models.ImageField(upload_to='course_receipts/', null=True, blank=True)
    payment_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_note = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user.username} → {self.course.title} [{self.payment_status}]'

    @property
    def is_approved(self):
        return self.payment_status == self.STATUS_APPROVED

    @property
    def is_pending(self):
        return self.payment_status == self.STATUS_PENDING

    @property
    def is_rejected(self):
        return self.payment_status == self.STATUS_REJECTED


# Keep old Enrollment as a thin alias so existing migrations don't break
class Enrollment(TimestampedModel):
    user   = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} enrolled in {self.course.title}'
