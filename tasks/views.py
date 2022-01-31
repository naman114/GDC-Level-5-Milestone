from django.http import HttpResponseRedirect
from django.shortcuts import render

from tasks.models import Task

active_tasks = []
completed_tasks = []

# Pending tasks
def tasks_view(request):
    active_tasks = Task.objects.filter(deleted=False, completed=False)
    search_term = request.GET.get("search")
    if search_term:
        active_tasks = active_tasks.filter(title__icontains=search_term)
    return render(request, "pending_tasks.html", {"tasks": active_tasks})


# Completed tasks
def completed_view(request):
    completed_tasks = Task.objects.filter(completed=True)
    search_term = request.GET.get("search")
    if search_term:
        completed_tasks = completed_tasks.filter(title__icontains=search_term)
    return render(request, "completed_tasks.html", {"tasks": completed_tasks})


# All tasks
def all_tasks_view(request):
    active_tasks = Task.objects.filter(deleted=False, completed=False)
    search_term = request.GET.get("search")
    if search_term:
        active_tasks = active_tasks.filter(title__icontains=search_term)

    completed_tasks = Task.objects.filter(completed=True)
    search_term = request.GET.get("search")
    if search_term:
        completed_tasks = completed_tasks.filter(title__icontains=search_term)
    return render(
        request,
        "all_tasks.html",
        {"active_tasks": active_tasks, "completed_tasks": completed_tasks},
    )


# Add a task
def add_task_view(request):
    task_to_add = request.GET.get("task")
    Task(title=task_to_add).save()
    return HttpResponseRedirect("/tasks")


# Delete a task
def delete_task_view(request, index):
    Task.objects.filter(id=index).update(deleted=True)
    return HttpResponseRedirect("/tasks")


# Mark task as complete
def complete_task_view(request, index):
    Task.objects.filter(id=index).update(completed=True)
    return HttpResponseRedirect("/tasks")
