from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Grievance, Comment , DepartmentHead

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class AssignGrievanceForm(forms.Form):
    department_head = forms.ModelChoiceField(
        queryset=DepartmentHead.objects.all(),  # Display all department heads
        empty_label="Select Department Head",   # Optional label for empty selection
        label="Department Head"                 # Field label
    )
    

class GrievanceForm(forms.ModelForm):
    class Meta:
        model = Grievance
        fields = ['grievance_type', 'description', 'priority', 'attachment']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']