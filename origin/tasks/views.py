from django.views.generic import ListView, CreateView, UpdateView
from tasks.forms import CreateTaskForm
from tasks.models import Task
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse


class ListTasksView(ListView):
    model = Task
    template_name = 'task_list.html'
    paginate_by = 30


class CreateTaskView(CreateView):
    form_class = CreateTaskForm
    template_name = 'create_task.html'
    success_url = reverse_lazy('tasks:task_list')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        # form_kwargs['user'] = self.request.user
        form_kwargs['user'] = User.objects.get()
        return form_kwargs


class EditTaskView(UpdateView):
    model = Task
    template_name = 'edit_task.html'
    success_url = reverse_lazy('tasks:task_list')
    fields = ['name', 'description']
