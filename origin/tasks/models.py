from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    TODO_STATUS = 'T'
    COMPLETED_STATUS = 'C'
    DELETED_STATUS = 'D'
    STATUSES = (
        (TODO_STATUS, 'To Do'),
        (COMPLETED_STATUS, 'Done'),
        (DELETED_STATUS, 'Deleted'),
    )
    created_by = models.ForeignKey(User, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    completed_by = models.ForeignKey(User, related_name='completed_tasks', null=True)
    completed_at = models.DateTimeField(default=timezone.now, null=True)
    deleted_by = models.ForeignKey(User, related_name='deleted_tasks', null=True)
    deleted_at = models.DateTimeField(default=timezone.now, null=True)
    status = models.CharField(max_length=1, choices=STATUSES, default=TODO_STATUS)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
