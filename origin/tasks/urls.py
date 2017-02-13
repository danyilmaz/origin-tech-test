from django.conf.urls import url

from tasks.views import ListTasksView, CreateTaskView, EditTaskView, MarkDoneStatusView, MarkNotDoneStatusView, DeleteTaskView

urlpatterns = [
    url(r'^create/$', CreateTaskView.as_view(), name='create_new'),
    url(r'^edit/(?P<pk>[\d]+)$', EditTaskView.as_view(), name='edit'),
    url(r'^mark_done/(?P<pk>[\d]+)$', MarkDoneStatusView.as_view(), name='mark_done'),
    url(r'^mark_not_done/(?P<pk>[\d]+)$', MarkNotDoneStatusView.as_view(), name='mark_not_done'),
    url(r'^delete/(?P<pk>[\d]+)$', DeleteTaskView.as_view(), name='delete'),
    url(r'^$', ListTasksView.as_view(), name='task_list'),
]
