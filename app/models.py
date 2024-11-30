from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Custom user model
class User(AbstractUser):
    # Custom fields for your user model (if any)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Specify unique related_name
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Specify unique related_name
        blank=True,
        help_text='Specific permissions for this user.'
    )

class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Department name (e.g., 'HR', 'TR')

    def __str__(self):
        return self.name  # Correctly returns the name of the department


# app/models.py
from django.conf import settings  # Ensure this is imported

class DepartmentHead(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        # Check if the department exists to avoid errors
        department_name = self.department.name if self.department else 'No Department Assigned'
        return f"{self.user.username} - {department_name}"

class Grievance(models.Model):
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('under_review', 'Under Review'),
        ('resolved', 'Resolved'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    GRIEVANCE_TYPES = [
        ('type1', 'Type 1'),
        ('type2', 'Type 2'),
        # Add more types as needed
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # The user who created the grievance
    grievance_type = models.CharField(max_length=50, choices=GRIEVANCE_TYPES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)  # Link grievance to department
    department_head = models.ForeignKey(DepartmentHead, null=True, blank=True, on_delete=models.SET_NULL)  # Department head handling the grievance
    description = models.TextField()  # Single description field
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    title = models.CharField(max_length=255, default="Untitled")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_grievances')  # User assigned to the grievance
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Comment(models.Model):
    grievance = models.ForeignKey(Grievance, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Feedback(models.Model):
    grievance = models.OneToOneField('Grievance', on_delete=models.CASCADE, related_name='feedback')
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='feedbacks')
    comments = models.TextField()
    rating = models.PositiveIntegerField()
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.grievance.title} by {self.submitted_by.username}"

