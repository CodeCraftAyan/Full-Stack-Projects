from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_tasks, name='dashboard'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_user, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('create-task/', views.create_task, name='create-task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit-task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete-task'),
]