from django.views.generic import ListView, CreateView, UpdateView, RedirectView, DeleteView
from tasks.forms import CreateTaskForm
from tasks.models import Task
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone


class ListTasksView(ListView):
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
    form_class = CreateTaskForm
    template_name = 'create_task.html'
    success_url = reverse_lazy('tasks:task_list')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs


class EditTaskView(UpdateView):
    model = Task
    template_name = 'edit_task.html'
    success_url = reverse_lazy('tasks:task_list')
    fields = ['name', 'description']

    def get_object(self):
        obj = get_object_or_404(Task, pk=self.kwargs['pk'], created_by=self.request.user)
        return obj


class BaseStatusToggleView(RedirectView):
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
    success_message = 'Task marked as Done'

    def update_task(self):
        self.object.status = Task.COMPLETED_STATUS
        self.object.completed_at = timezone.now()
        self.object.completed_by = self.request.user


class MarkNotDoneStatusView(BaseStatusToggleView):
    success_message = 'Task marked as To Do'

    def update_task(self):
        self.object.status = Task.TODO_STATUS
        self.object.completed_at = None
        self.object.completed_by = None


class DeleteTaskView(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task_list')
    template_name = 'delete_lender.html'

    def delete(self, request, *args, **kwargs):
        self.object = get_object_or_404(Task, pk=self.kwargs['pk'], created_by=self.request.user)
        success_url = self.get_success_url()
        self.object.delete(user=request.user)
        return HttpResponseRedirect(success_url)
