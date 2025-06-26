from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import UserProfile, Task
from .forms import UserProfileForm, RegisterForm, TaskForm

# ✅ User Login View
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            try:
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={'name': user.username, 'email': user.email, 'role': 'user'}
                )
                profile.last_login = now()
                profile.save()
                messages.success(request, "✅ Logged in successfully!")
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f"Profile error: {e}")
                return render(request, "myapp/login.html", {"error": f"Profile error: {e}"})
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "myapp/login.html", {"error": "Invalid credentials"})
    return render(request, "myapp/login.html")

# ✅ User Logout View
def user_logout(request):
    logout(request)
    messages.success(request, "✅ Logged out successfully!")
    return redirect('login')

# ✅ Dashboard View (Task + User Overview)
@login_required
def dashboard(request):
    user_query = request.GET.get('user_query', '')
    task_query = request.GET.get('task_query', '')
    status = request.GET.get('status', 'all')
    
    users = UserProfile.objects.filter(name__icontains=user_query) if user_query else UserProfile.objects.all()

    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('login')

    if user_profile.role == "admin":
        user_tasks = Task.objects.all()
    else:
        user_tasks = Task.objects.filter(user=request.user)

    if task_query:
        user_tasks = user_tasks.filter(title__icontains=task_query) | user_tasks.filter(description__icontains=task_query)
    
    if status == 'completed':
        user_tasks = user_tasks.filter(is_completed=True)
    elif status == 'pending':
        user_tasks = user_tasks.filter(is_completed=False)
    
    user_tasks = user_tasks.order_by('-created_at')
    tasks_completed = user_tasks.filter(is_completed=True).count()
    tasks_pending = user_tasks.count() - tasks_completed

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
            messages.error(request, "❌ Invalid task data. Please check the form.")

    active_sessions = Session.objects.filter(expire_date__gte=now())
    online_user_ids = [s.get_decoded().get('_auth_user_id') for s in active_sessions]
    users_online = User.objects.filter(id__in=online_user_ids).count()

    # Recent activity (simulated for now, as no activity model exists)
    recent_activities = []
    for task in user_tasks[:5]:  # Show last 5 tasks as activities
        recent_activities.append({
            'action': 'created' if not task.is_completed else 'completed',
            'message': f"Task '{task.title}' {'created' if not task.is_completed else 'completed'} by {task.user.username}",
            'timestamp': task.created_at
        })

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

# ✅ Task Views
@login_required
def complete_task(request, task_id):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('login')

    if user_profile.role == "admin":
        task = get_object_or_404(Task, id=task_id)  # Admins can complete any task
    else:
        task = get_object_or_404(Task, id=task_id, user=request.user)  # Non-admins can only complete their own tasks
    
    task.is_completed = True
    task.save()
    messages.success(request, "🎉 Task marked as completed!")
    return redirect('dashboard')

@login_required
@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, "🗑️ Task deleted successfully!")
    return redirect('dashboard')

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "✏️ Task updated successfully!")
        return redirect('dashboard')
    return render(request, "myapp/edit_task.html", {"form": form, "task": task})

# ✅ Register New Users
def register_user(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
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

# ✅ Edit User Profile (Admin Only)
@login_required
def edit_profile(request, user_id):
    try:
        if request.user.userprofile.role != "admin":
            messages.error(request, "❌ You are not authorized to edit profiles.")
            return redirect("dashboard")
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('login')

    profile = get_object_or_404(UserProfile, user__id=user_id)
    form = UserProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"👤 {profile.user.username}'s profile updated!")
        return redirect("dashboard")
    return render(request, "myapp/edit_profile.html", {"form": form, "user": profile})

# ✅ Delete User Profile (Admin Only)
@login_required
def delete_user(request, user_id):
    try:
        if request.user.userprofile.role != "admin":
            messages.error(request, "❌ You are not authorized to delete users.")
            return redirect("dashboard")
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('login')

    profile = get_object_or_404(UserProfile, user__id=user_id)
    if request.method == "POST":
        profile.user.delete()
        messages.success(request, f"❌ {profile.name}'s account deleted.")
        return redirect("dashboard")
    return render(request, "myapp/delete_confirm.html", {"user": profile})