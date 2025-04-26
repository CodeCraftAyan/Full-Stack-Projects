from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib import messages

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            error_message = "Invalid username or password. please try again."
            return render(request, 'login.html', {
                'show_auth_nav':True,
                'error_message':error_message
            })
    return render(request, 'login.html', {'show_auth_nav':True})

def signup_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if password != confirmPassword:
            error_message = "Passwords do not match. Please try again."
            return render(request, 'signup.html', {'show_auth_nav': True, 'error_message': error_message})

        if User.objects.filter(email=email).exists():
            error_message = "This Email already taken. Choose a different one."
            return render(request, 'signup.html', {'show_auth_nav': True, 'error_message': error_message})

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user)
            return redirect('dashboard')
        except IntegrityError:
            error_message = "Error creating account. Try again later."
            return render(request, 'signup.html', {'show_auth_nav': True, 'error_message': error_message})

    return render(request, 'signup.html', {'show_auth_nav': True})


def logout_user(request):
    logout(request)
    return redirect('/')

@login_required
def view_tasks(request):
    color_mapping = {
        'urgent-important': 'rose',
        'important-not-urgent': 'yellow',
        'urgent-not-important': 'blue',
        'neither': 'gray'
    }

    tasks = Task.objects.filter(user=request.user)

    for task in tasks:
        task.bg_color = color_mapping.get(task.priority, 'gray')

    return render(request, 'view-tasks.html', {
        'show_auth_nav':False,
        'tasks':tasks,
    }) 

@login_required
def create_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        time = request.POST.get('time')
        priority = request.POST.get('priority', 'neither')
        
        if title and time:
            Task.objects.create(
                user=request.user,
                title=title,
                description=description,
                time=time,
                priority=priority
            )
            messages.success(request, 'Task added successfully!')
            return redirect('/')
        else:
            error_message = "Title and Time are required!"
            return render(request, 'add-task.html', {
                'show_auth_nav':False,
                'error_message':error_message
            })

    return render(request, 'add-task.html', {'show_auth_nav':False})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.time = request.POST.get('time')
        task.priority = request.POST.get('priority')
        task.status = request.POST.get('status') == 'on'

        task.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('/')
    
    return render(request, 'edit-task.html', {
        'show_auth_nav':False,
        'task':task
    })


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, 'Task Deleted Successfuly!')
    return redirect('/')