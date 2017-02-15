from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    """A task in the todo list.
    """
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
    completed_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, related_name='deleted_tasks', null=True)
    deleted_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=1, choices=STATUSES, default=TODO_STATUS)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    @property
    def is_done(self):
        """A property to tell us whether we should consider a task done or not based on its status
        """
        if self.status in [self.DELETED_STATUS, self.COMPLETED_STATUS]:
            return True
        return False

    def delete(self, user):
        """Custom delete method. We only want to mark tasks as deleted so that the history of the database makes sense
        """
        self.deleted_at = timezone.now()
        self.status = self.DELETED_STATUS
        self.deleted_by = user
        self.save()
