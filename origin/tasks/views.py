from django.views.generic import ListView, CreateView, UpdateView, RedirectView, DeleteView
from tasks.forms import CreateTaskForm
from tasks.models import Task
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404


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


class BaseStatusToggleView(RedirectView):
    """Base view to set the mandate active or inactive.
    Child classes should inherit from this view and provide a boolean 'is_active'
    attribute and a string 'success_message' attribute.
    """
    status = None
    success_message = None

    def get_redirect_url(self):
        return reverse_lazy('tasks:task_list')

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        task.status = self.status
        task.save()
        messages.success(request, self.success_message)
        return HttpResponseRedirect(self.get_redirect_url())


class MarkDoneStatusView(BaseStatusToggleView):
    status = Task.COMPLETED_STATUS
    success_message = 'Task marked as Done'


class MarkNotDoneStatusView(BaseStatusToggleView):
    status = Task.TODO_STATUS
    success_message = 'Task marked as To Do'


class DeleteTaskView(DeleteView):
    model = Lender
    success_url = reverse_lazy('lender:list_lenders')
    pk_url_kwarg = 'lender_pk'
    template_name = 'delete_lender.html'

    def delete(self, request, *args, **kwargs):
        http_response = super(DeleteLenderView, self).delete(request, *args, **kwargs)
        for lend_order in self.object.lend_orders.filter(deleted_at__isnull=True):
            lend_order.deleted_at = datetime.datetime.now()
            lend_order.save()
        return JsonResponse(dict(url=http_response.url), status=200)
