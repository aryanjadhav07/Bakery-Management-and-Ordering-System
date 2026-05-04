from django.contrib import admin
from django.contrib.auth.models import User
from .models import *

# ✅ Register default Django User safely


# ✅ Register all your models
admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(Course)
admin.site.register(Product)
admin.site.register(Enrollment)
admin.site.register(ChatMessage)
admin.site.register(ClassSchedule)