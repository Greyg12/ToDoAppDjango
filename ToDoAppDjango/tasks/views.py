from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib import messages
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        progress = request.POST.get('progress')
        completed_at = request.POST.get('completed_at')  # Updated field name

        if not completed_at:
            messages.error(request, 'Completion date and time is required.')
            return render(request, 'tasks/create_task.html', {
                'title': title,
                'description': description,
                'progress': progress,
                'today': now()
            })

        Task.objects.create(
            title=title,
            description=description,
            progress=progress,
            completed_at=completed_at  # Updated field name
        )
        return redirect('task_list')
    return render(request, 'tasks/create_task.html', {'today': now()})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.progress = request.POST.get('progress')
        task.save()
        return redirect('task_list')  # Redirect to the task list after editing
    return render(request, 'tasks/edit_task.html', {'task': task})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')  # Redirect to the task list after deletion
    return render(request, 'tasks/delete_task.html', {'task': task})
