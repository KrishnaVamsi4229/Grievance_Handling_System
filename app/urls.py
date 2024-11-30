from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),

    path('create_grievance/', views.create_grievance, name='create_grievance'),
    path('grievance_list/', views.grievance_list, name='grievance_list'),
    path('assign_grievance/<int:grievance_id>/', views.assign_grievance, name='assign_grievance'),
    path('change_status/<int:grievance_id>/', views.change_status, name='change_status'),

    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('department_head_dashboard/', views.department_head_dashboard, name='department_head_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_summary/', views.admin_summary, name='admin_summary'),
    path('department_summary/', views.department_summary, name='department_summary'),
    path('department_head_summary/', views.department_summary, name='department_head_summary'),
    path('admin_or_department_summary/', views.admin_summary, name='admin_or_department_summary'),
    path('feedback/submit/<int:grievance_id>/', views.feedback_submit, name='feedback_submit'),

    
]