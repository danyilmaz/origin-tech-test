from django.conf.urls import url

from tasks.views import ListTasksView, CreateTaskView, EditTaskView

urlpatterns = [
    url(r'^create/$', CreateTaskView.as_view(), name='create_new'),
    url(r'^edit/(?P<pk>[\d]+)$', EditTaskView.as_view(), name='edit'),
    url(r'^$', ListTasksView.as_view(), name='task_list'),
]
