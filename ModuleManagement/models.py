from django.db import models

class Module(models.Model):
    name = models.CharField(max_length=100, default='', blank=True)
    order = models.IntegerField(null=True)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100, default='', blank=True)
    order = models.IntegerField(null=True)
    task_url = models.CharField(max_length=50, default='', blank=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, blank=True)
    view_task = models.BooleanField(default=False)
    add_task = models.BooleanField(default=False)
    save_task = models.BooleanField(default=False)
    edit_task = models.BooleanField(default=False)
    delete_task = models.BooleanField(default=False)
    print_task = models.BooleanField(default=False)
    cancel_task = models.BooleanField(default=False)
    reset_task = models.BooleanField(default=False)
    find_task = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "Task:"+self.name

    class Meta:
        ordering = ['order']

