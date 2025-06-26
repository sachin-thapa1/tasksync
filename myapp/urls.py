from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('task/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('register/', views.register_user, name='register'),  # Changed to 'register'
    path('profile/<int:user_id>/edit/', views.edit_profile, name='edit_profile'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
]