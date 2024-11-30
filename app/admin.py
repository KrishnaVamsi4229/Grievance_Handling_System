from django.contrib import admin
from .models import User, DepartmentHead, Grievance, Comment

admin.site.register(User)
admin.site.register(DepartmentHead)
admin.site.register(Grievance)
admin.site.register(Comment)
