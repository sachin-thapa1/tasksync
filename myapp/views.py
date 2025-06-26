from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q

from .models import UserProfile, Task
from .forms import UserProfileForm, RegisterForm, TaskForm

# User Login View
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Create or update UserProfile
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'name': user.username,
                    'email': user.email,
                    'role': 'admin' if user.is_superuser else 'user'
                }
            )
            if not created and user.is_superuser:
                profile.role = 'admin'  # Ensure superusers have admin role
                profile.save()
            profile.last_login = now()
            profile.save()
            messages.success(request, "✅ Logged in successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "❌ Invalid username or password.")
    return render(request, "myapp/login.html")

# User Logout View
def user_logout(request):
    logout(request)
    messages.success(request, "✅ Logged out successfully!")
    return redirect('login')

# Dashboard View
@login_required
def dashboard(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('login')

    user_query = request.GET.get('user_query', '')
    task_query = request.GET.get('task_query', '')
    status = request.GET.get('status', 'all')

    # Admin or superuser sees all users and tasks
    if user_profile.role == "admin" or request.user.is_superuser:
        users = UserProfile.objects.filter(name__icontains=user_query) if user_query else UserProfile.objects.all()
        user_tasks = Task.objects.all()
    else:
        users = UserProfile.objects.filter(user=request.user)
        user_tasks = Task.objects.filter(user=request.user)

    # Filter tasks by search
    if task_query:
        user_tasks = user_tasks.filter(
            Q(title__icontains=task_query) | Q(description__icontains=task_query)
        )

    # Filter tasks by status
    if status == 'completed':
        user_tasks = user_tasks.filter(is_completed=True)
    elif status == 'pending':
        user_tasks = user_tasks.filter(is_completed=False)

    user_tasks = user_tasks.order_by('-created_at')
    tasks_completed = user_tasks.filter(is_completed=True).count()
    tasks_pending = user_tasks.count() - tasks_completed

    # Handle task creation
    task_form = TaskForm()
    if request.method == "POST" and 'add_task' in request.POST:
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            new_task = task_form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            messages.success(request, "✅ Task added successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "❌ Invalid task data.")

    # Active sessions / users online
    active_sessions = Session.objects.filter(expire_date__gte=now())
    online_user_ids = [s.get_decoded().get('_auth_user_id') for s in active_sessions]
    users_online = User.objects.filter(id__in=online_user_ids).count()

    # Recent activity
    recent_activities = [{
        'action': 'completed' if task.is_completed else 'created',
        'message': f"Task '{task.title}' {'completed' if task.is_completed else 'created'} by {task.user.username}",
        'timestamp': task.created_at
    } for task in user_tasks[:5]]

    return render(request, "myapp/home.html", {
        "users": users,
        "user_query": user_query,
        "task_query": task_query,
        "status": status,
        "users_online": users_online,
        "user_tasks": user_tasks,
        "tasks_completed": tasks_completed,
        "tasks_pending": tasks_pending,
        "task_form": task_form,
        "recent_activities": recent_activities,
    })

# Complete Task
@login_required
def complete_task(request, task_id):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('login')

    # Allow admins to complete any task, others only their own
    task_filter = {} if (user_profile.role == "admin" or request.user.is_superuser) else {'user': request.user}
    task = get_object_or_404(Task, id=task_id, **task_filter)

    task.is_completed = True
    task.save()
    messages.success(request, "🎉 Task marked as completed!")
    return redirect('dashboard')

# Delete Task
@login_required
@require_POST
def delete_task(request, task_id):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('login')

    # Allow admins to delete any task, others only their own
    task_filter = {} if (user_profile.role == "admin" or request.user.is_superuser) else {'user': request.user}
    task = get_object_or_404(Task, id=task_id, **task_filter)
    task.delete()
    messages.success(request, "🗑️ Task deleted successfully!")
    return redirect('dashboard')

# Edit Task
@login_required
def edit_task(request, task_id):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('login')

    # Allow admins to edit any task, others only their own
    task_filter = {} if (user_profile.role == "admin" or request.user.is_superuser) else {'user': request.user}
    task = get_object_or_404(Task, id=task_id, **task_filter)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "✏️ Task updated successfully!")
        return redirect('dashboard')
    return render(request, "myapp/edit_task.html", {"form": form, "task": task})

# Register User
def register_user(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        if not UserProfile.objects.filter(user=user).exists():
            UserProfile.objects.create(
                user=user,
                name=user.username,
                email=user.email,
                role='user'
            )
        login(request, user)
        messages.success(request, "✅ Registration successful!")
        return redirect("dashboard")
    return render(request, "myapp/register.html", {"form": form})

# Admin: Edit User Profile
@login_required
def edit_profile(request, user_id):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('login')

    if not (user_profile.role == "admin" or request.user.is_superuser):
        messages.error(request, "❌ Unauthorized access.")
        return redirect("dashboard")

    profile = get_object_or_404(UserProfile, user__id=user_id)
    form = UserProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"👤 {profile.user.username}'s profile updated!")
        return redirect("dashboard")
    return render(request, "myapp/edit_profile.html", {"form": form, "user": profile})

# Admin: Delete User
@login_required
def delete_user(request, user_id):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('login')

    if not (user_profile.role == "admin" or request.user.is_superuser):
        messages.error(request, "❌ Unauthorized access.")
        return redirect("dashboard")

    profile = get_object_or_404(UserProfile, user__id=user_id)
    if request.method == "POST":
        profile.user.delete()
        messages.success(request, f"❌ {profile.name}'s account deleted.")
        return redirect("dashboard")
    return render(request, "myapp/confirm_delete_user.html", {"user": profile})