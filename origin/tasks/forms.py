from django.forms import ModelForm
from tasks.models import Task


class CreateTaskForm(ModelForm):
    """Custom create task form

    This form takes a user object when it is initialised.
    On form.save, we write that user to the  'created_by' field
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.created_by = self.user
        return super().save(*args, **kwargs)

    class Meta:
        model = Task
        fields = ['name', 'description']
