# todo/urls.py
from django.urls import path
from .views import TaskListView, TaskDetailView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<str:task_id>/', TaskDetailView.as_view(), name='task-detail'),
]
