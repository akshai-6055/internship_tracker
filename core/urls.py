from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
    
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('internship/create/', views.create_internship, name='create_internship'),
    path('internship/<int:pk>/edit/', views.edit_internship, name='edit_internship'),
    path('internship/<int:pk>/delete/', views.delete_internship, name='delete_internship'),
    path('application/<int:pk>/update_status/', views.update_application_status, name='update_application_status'),
    
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('internships/', views.student_internships, name='student_internships'),
    path('internship/<int:pk>/apply/', views.apply_internship, name='apply_internship'),
    path('application/<int:pk>/edit/', views.edit_application, name='edit_application'),
    path('application/<int:pk>/withdraw/', views.withdraw_application, name='withdraw_application'),
]
