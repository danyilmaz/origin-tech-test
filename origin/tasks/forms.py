from django.forms import ModelForm
from tasks.models import Task


class CreateTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.created_by = self.user
        return super().save(*args, **kwargs)

    class Meta:
        model = Task
        fields = ['name', 'description']
