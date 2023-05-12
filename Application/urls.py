from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('qualifications/<int:contact_id>/', views.qualification, name='qualification'),
    path('application/<int:contact_id>/<int:program_id>/', views.application, name='application'),
    # path('application/success/', views.application_success, name='application_success')

]