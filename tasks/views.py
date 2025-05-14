from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if not title:
            messages.error(request, "Task name can't be empty")
            return redirect('task_list')
        Task.objects.create(title=title, user=request.user)
        return redirect('task_list')

    search = request.GET.get('search', '')
    filter_type = request.GET.get('filter', 'all')

    if search:
        tasks = tasks.filter(title__icontains=search)

    if filter_type == 'done':
        tasks = tasks.filter(completed=True)
    elif filter_type == 'undone':
        tasks = tasks.filter(completed=False)

    context = {
        'tasks': tasks,
        'search': search,
        'filter_type': filter_type,
        'done_count': Task.objects.filter(user=request.user, completed=True).count(),
        'todo_count': Task.objects.filter(user=request.user, completed=False).count(),
    }
    return render(request, 'task_list.html', context)

@login_required
def toggle_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

@login_required
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')
