from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from model_mommy import mommy
from tasks.models import Task


class TestTaskModel(TestCase):
    def test_delete(self):
        """Test that the delete function leaves the object in tact but changes
        the status and marks who it was deleted by and when.
        """
        task = mommy.make(Task, pk=100, deleted_by=None, deleted_at=None, status=Task.TODO_STATUS)
        user = mommy.make(User)
        frozen_datetime = datetime(2017, 2, 15, tzinfo=timezone.utc)
        with freeze_time(frozen_datetime):
            task.delete(user)
            task.refresh_from_db()
            self.assertEqual(task.deleted_by, user)
            self.assertEqual(task.deleted_at, frozen_datetime)
            self.assertEqual(task.status, Task.DELETED_STATUS)
            self.assertEqual(Task.objects.get(pk=100), task)

    def test_todo_task_is_not_done(self):
        """Test that tasks with a TODO_STATUS are not 'done'
        """
        todo_task = mommy.make(Task, status=Task.TODO_STATUS)
        self.assertFalse(todo_task.is_done)

    def test_completed_task_is_done(self):
        """Test that tasks with a COMPLETED_STATUS are 'done'
        """
        completed_task = mommy.make(Task, status=Task.COMPLETED_STATUS)
        self.assertTrue(completed_task.is_done)

    def test_deleted_task_is_done(self):
        """Test that tasks with a DELETED_STATUS are 'done'
        """
        deleted_task = mommy.make(Task, status=Task.DELETED_STATUS)
        self.assertTrue(deleted_task.is_done)
