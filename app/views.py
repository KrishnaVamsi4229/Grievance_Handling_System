from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegistrationForm, GrievanceForm, CommentForm , AssignGrievanceForm
from .models import DepartmentHead, User, Grievance, Comment , Feedback
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse  
from app.models import Department, DepartmentHead, Grievance


def is_superuser(user):
    return user.is_superuser

def is_staff(user):
    return user.is_staff

def index(request):
    return render(request,"app/home.html")

from django.shortcuts import render
from app.models import Grievance

def admin_summary(request):
    # Get the count of grievances for each status
    received = Grievance.objects.filter(status='received').count()
    under_review = Grievance.objects.filter(status='under_review').count()
    resolved = Grievance.objects.filter(status='resolved').count()

    # Pass the data to the template
    context = {
        'received': received,
        'under_review': under_review,
        'resolved': resolved,
    }
    return render(request, 'app/admin_or_department_summary.html', context)

@login_required
@user_passes_test(lambda user: hasattr(user, 'departmenthead'))
def department_summary(request):
    # Get the grievances associated with the current department head's department
    department_head = request.user.departmenthead
    # Fetch grievances assigned to this department head (and not the whole department)
    grievances = Grievance.objects.filter(department_head=department_head)
    # Calculate summary statistics
    received = grievances.filter(status='received').count()
    under_review = grievances.filter(status='under_review').count()
    resolved = grievances.filter(status='resolved').count()
    total_grievances = grievances.count()

    # Pass data to the template
    context = {
        'received': received,
        'under_review': under_review,
        'resolved': resolved,
        'total_grievances': total_grievances,
    }
    return render(request, 'app/department_head_summary.html', context)


@login_required
def dashboard_redirect(request):
    # Redirect to appropriate dashboard based on user role
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    elif request.user.is_staff:
        return redirect('department_head_dashboard')
    else:
        return redirect('user_dashboard')

@login_required
def user_dashboard(request):
    grievances = Grievance.objects.filter(user=request.user)
    return render(request, 'app/user_dashboard.html', {'grievances': grievances})


@login_required
@user_passes_test(is_superuser)
def admin_dashboard(request):
    grievances = Grievance.objects.all()
    paginator = Paginator(grievances, 10)  # Show 10 grievances per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/admin_dashboard.html', {'page_obj': page_obj})

@login_required
@user_passes_test(is_staff)
def department_head_dashboard(request):
    department = request.user.departmenthead.department
    # Get the grievances assigned to the current logged-in user
    grievances = Grievance.objects.filter(assigned_to=request.user)
    feedbacks = Feedback.objects.filter(department=department)

    return render(request, 'app/department_head_dashboard.html', {'grievances': grievances , 'feedbacks': feedbacks})

def register(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login page
            return redirect(reverse('login'))  # Use the name of your login URL pattern
    return render(request, 'app/register.html', {'form': form})


@login_required
def create_grievance(request):
    if request.method == 'POST':
        form = GrievanceForm(request.POST, request.FILES)
        if form.is_valid():
            grievance = form.save(commit=False)
            grievance.user = request.user
            grievance.save()
            return redirect('user_dashboard')
    else:
        form = GrievanceForm()
    return render(request, 'app/create_grievance.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def grievance_list(request):
    grievances = Grievance.objects.all()  # Or apply any necessary filtering
    paginator = Paginator(grievances, 10)  # Display 10 grievances per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'app/grievance_list.html', {'page_obj': page_obj})

from app.models import DepartmentHead

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from app.models import Department, DepartmentHead, Grievance
from django.contrib.auth import get_user_model

@login_required
@user_passes_test(is_superuser)
def assign_grievance(request, grievance_id):
    grievance = get_object_or_404(Grievance, id=grievance_id)
    department_heads = DepartmentHead.objects.select_related('user', 'department').all()

    success_message = None  # Initialize message variable

    if request.method == "POST":
        selected_department_name = request.POST.get("department_head")
        selected_department = Department.objects.filter(name=selected_department_name).first()

        if selected_department:
            # Fetch the department head of the selected department
            department_head = DepartmentHead.objects.filter(department=selected_department).first()

            if department_head:
                # Assign the grievance to the department head and the department
                grievance.assigned_to = department_head.user
                grievance.department = selected_department  # Assign department to grievance
                grievance.save()

                # Provide feedback to the user
                success_message = f"Grievance {grievance_id} has been successfully assigned to {department_head.user.username}"
            else:
                success_message = f"No department head found for {selected_department_name}"
        else:
            success_message = f"Department {selected_department_name} not found"

    return render(request, "app/assign_grievance.html", {
        "grievance": grievance,
        "department_heads": department_heads,
        "message": success_message,  # Pass the message to template
    })



@login_required
@user_passes_test(is_superuser)
def change_status(request, grievance_id):
    grievance = get_object_or_404(Grievance, id=grievance_id)
    if request.method == 'POST':
        grievance.status = request.POST['status']
        grievance.save()
        comment = Comment(grievance=grievance, author=request.user, text=request.POST['comment'])
        comment.save()
        return redirect('admin_dashboard')
    
    # send_mail(
    #     subject='Grievance Status Update',
    #     message=f'Your grievance status has been updated to: {grievance.status}',
    #     from_email=settings.EMAIL_HOST_USER,
    #     recipient_list=[grievance.user.email],
    # )

    return render(request, 'app/change_status.html', {'grievance': grievance})

def feedback(request):
    return render(request,"app/feedback.html")


@login_required
def feedback_submit(request, grievance_id):
    grievance = get_object_or_404(Grievance, id=grievance_id)

    # Ensure the grievance is assigned to a department
    if not grievance.department:
        return HttpResponse("Grievance is not assigned to any department.")

    department = grievance.department  # Fetch the department the grievance is linked to

    if request.method == 'POST':
        comments = request.POST.get('comments')
        rating = request.POST.get('rating')

        # Validate rating
        if not rating.isdigit() or int(rating) < 1 or int(rating) > 10:
            return HttpResponse("Rating must be between 1 and 10.")

        # Check if feedback already exists
        if Feedback.objects.filter(grievance=grievance).exists():
            return HttpResponse("Feedback for this grievance has already been submitted.")

        # Save feedback
        Feedback.objects.create(
            grievance=grievance,
            department=department,  # Link feedback to the department
            comments=comments,
            rating=int(rating),
            submitted_by=request.user
        )

        return HttpResponse("Thank you for your feedback!")

    return render(request, "app/feedback_submit.html", {'grievance': grievance})




