from django.db import models
from django.contrib.auth.models import User
from core.models import TimestampedModel

class Course(TimestampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught', null=True, blank=True)

    def __str__(self):
        return self.title

class Enrollment(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} enrolled in {self.course.title}'
