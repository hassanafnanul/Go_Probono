from django.urls import path
from . import module_views, task_views

urlpatterns = [
    path('modules/', module_views.ModuleManagement, name='ModuleManagement'),
    # path('modules/add/', module_views.ModuleCreate, name='ModuleCreate'),
    # path('modules/view/<int:id>/', module_views.ModuleView, name='ModuleView'),
    # path('modules/edit/<int:id>/', module_views.ModuleEdit, name='ModuleEdit'),

    # path('tasks/', task_views.TaskManagement, name='TaskManagement'),
    # path('tasks/add/', task_views.TaskCreate, name='TaskCreate'),
    # path('tasks/view/<int:id>/', task_views.TaskView, name='TaskView'),
    # path('tasks/edit/<int:id>/', task_views.TaskEdit, name='TaskEdit'),
]