from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from tasks.views import ListTasksView, CreateTaskView, EditTaskView, MarkDoneStatusView, MarkNotDoneStatusView, DeleteTaskView

urlpatterns = [
    url(r'^create/$', login_required(CreateTaskView.as_view()), name='create_new'),
    url(r'^edit/(?P<pk>[\d]+)$', login_required(EditTaskView.as_view()), name='edit'),
    url(r'^mark_done/(?P<pk>[\d]+)$', login_required(MarkDoneStatusView.as_view()), name='mark_done'),
    url(r'^mark_not_done/(?P<pk>[\d]+)$', login_required(MarkNotDoneStatusView.as_view()), name='mark_not_done'),
    url(r'^delete/(?P<pk>[\d]+)$', login_required(DeleteTaskView.as_view()), name='delete'),
    url(r'^todo/$', login_required(ListTasksView.as_view(hide_completed=True)), name='task_list_hide_completed'),
    url(r'^$', login_required(ListTasksView.as_view()), name='task_list'),
]
