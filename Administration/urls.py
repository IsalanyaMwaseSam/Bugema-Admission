from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('approved-applications/', views.ApprovedApplications, name='approved-applications'),
    path('rejected-applications/', views.RejectedApplications, name='rejected-applications'),
    path('pending-applications/', views.PendingApplications, name='pending-applications'),
    path('approve/<int:application_id>/', views.approve_application, name='approve_application'),
    path('reject/<int:application_id>/', views.reject_application, name='reject_application'),
]