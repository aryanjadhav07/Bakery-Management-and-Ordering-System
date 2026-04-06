from django.db import models
from courses.models import Course
from core.models import TimestampedModel

class ClassSchedule(TimestampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f'{self.course.title} at {self.start_time}'
