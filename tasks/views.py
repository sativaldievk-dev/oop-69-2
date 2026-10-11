from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import TaskForm
from .models import Task


def task_list(request):
    tasks = Task.objects.order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {'form': form})


def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.completed = not task.completed
        task.save(update_fields=['completed'])

        next_url = request.POST.get('next')
        if next_url:
            return redirect(next_url)

        return redirect(reverse('tasks:task_detail', args=[task.pk]))

    return redirect('tasks:task_list')
