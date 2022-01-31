from django.http import HttpResponseRedirect
from django.shortcuts import render

from tasks.models import Task

# Pending tasks
def tasks_view(request):
    search_term = request.GET.get("search")
    return render(
        request, "pending_tasks.html", {"tasks": get_tasks("pending", search_term)}
    )


# Completed tasks
def completed_view(request):
    search_term = request.GET.get("search")
    return render(
        request, "completed_tasks.html", {"tasks": get_tasks("completed", search_term)}
    )


# All tasks
def all_tasks_view(request):
    search_term = request.GET.get("search")
    return render(
        request,
        "all_tasks.html",
        {
            "active_tasks": get_tasks("pending", search_term),
            "completed_tasks": get_tasks("completed", search_term),
        },
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


# Helper function to return pending tasks and completed tasks
def get_tasks(task_type, search_term):
    tasks = None
    if task_type == "pending":
        tasks = Task.objects.filter(deleted=False, completed=False)
    elif task_type == "completed":
        tasks = Task.objects.filter(completed=True)

    if search_term:
        tasks = tasks.filter(title__icontains=search_term)

    return tasks
