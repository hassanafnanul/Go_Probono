from django.db import models
from django.contrib.auth.models import User
import random
import string
# from Go_Probono.utils import randomStringGenerator
from RoleCreation.models import Role
from ModuleManagement.models import Task


class UserWithRole(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
    role = models.ForeignKey(Role,on_delete=models.SET_NULL,null=True,blank=True)
    picture = models.ImageField(upload_to='userimg/', default='media/userimg/default.png')
    mobile = models.CharField(max_length=15,null=True,blank=True)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return 'No user found'


class UserWithTask(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    task = models.ForeignKey(Task,on_delete=models.SET_NULL,null=True,blank=True)
    view_task = models.BooleanField(default=False)
    add_task = models.BooleanField(default=False)
    save_task = models.BooleanField(default=False)
    edit_task = models.BooleanField(default=False)
    delete_task = models.BooleanField(default=False)
    print_task = models.BooleanField(default=False)
    cancel_task = models.BooleanField(default=False)
    reset_task = models.BooleanField(default=False)
    find_task = models.BooleanField(default=False)
    home_task = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        if self.user and self.task:
            return self.user.username+'->'+self.task.name
        else:
            return 'User / Task not available'
