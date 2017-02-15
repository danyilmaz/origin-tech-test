from django.views.generic import ListView, CreateView, UpdateView, RedirectView, DeleteView
from tasks.forms import CreateTaskForm
from tasks.models import Task
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone


class ListTasksView(ListView):
    """List view for all tasks.
    we always hide 'deleted' tasks.
    optionally hide completed tasks.
    """
    model = Task
    template_name = 'task_list.html'
    paginate_by = 30
    hide_completed = False
    queryset = Task.objects.exclude(status=Task.DELETED_STATUS)

    def get_queryset(self):
        if self.hide_completed:
            return Task.objects.exclude(status__in=[Task.DELETED_STATUS, Task.COMPLETED_STATUS])
        return Task.objects.exclude(status=Task.DELETED_STATUS)


class CreateTaskView(CreateView):
    """View for creating new tasks.
    """
    form_class = CreateTaskForm
    template_name = 'create_task.html'
    success_url = reverse_lazy('tasks:task_list')

    def get_form_kwargs(self):
        """Pass the logged in user to the form. This is safer than doing something
        nasty with hidden fields.
        """
        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs


class EditTaskView(UpdateView):
    """View to allow editing of tasks.
    """
    model = Task
    template_name = 'edit_task.html'
    success_url = reverse_lazy('tasks:task_list')
    fields = ['name', 'description']

    def get_object(self):
        """We override get object here so we can pass it the logged in user.
        This ensures that users can only edit tasks they have created.
        """
        obj = get_object_or_404(Task, pk=self.kwargs['pk'], created_by=self.request.user)
        return obj


class BaseStatusToggleView(RedirectView):
    """Base view which updates a task's status.
    Both marking as Done and makring as Not Done share a lot of similar code
    This is DRYer
    """
    success_message = None

    def get_redirect_url(self):
        return reverse_lazy('tasks:task_list')

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(Task, pk=self.kwargs['pk'])
        self.update_task()
        self.object.save()
        messages.success(request, self.success_message)
        return HttpResponseRedirect(self.get_redirect_url())


class MarkDoneStatusView(BaseStatusToggleView):
    """Child view to mark a task as done.
    """
    success_message = 'Task marked as Done'

    def update_task(self):
        self.object.status = Task.COMPLETED_STATUS
        self.object.completed_at = timezone.now()
        self.object.completed_by = self.request.user


class MarkNotDoneStatusView(BaseStatusToggleView):
    """Child view to mark a task as Todo
    """
    success_message = 'Task marked as To Do'

    def update_task(self):
        self.object.status = Task.TODO_STATUS
        self.object.completed_at = None
        self.object.completed_by = None


class DeleteTaskView(DeleteView):
    """Delete view to mark a task as deleted.
    """
    model = Task
    success_url = reverse_lazy('tasks:task_list')
    template_name = 'delete_lender.html'

    def delete(self, request, *args, **kwargs):
        """Override this method, as we want to persist the object in the db for audit reasons.

        get_object_or_404 allows us to be confident that users may only delete tasks
        they themselves have created
        """
        self.object = get_object_or_404(Task, pk=self.kwargs['pk'], created_by=self.request.user)
        success_url = self.get_success_url()
        self.object.delete(user=request.user)
        return HttpResponseRedirect(success_url)
