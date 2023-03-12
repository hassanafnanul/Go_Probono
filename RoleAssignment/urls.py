from django.urls import path
from . import views

urlpatterns = [
    path('', views.RoleAssignment, name='UserManagement'),
    path('add/', views.NewRoleAssign, name='NewRoleAssign'),
    path('edit/<int:id>', views.Edit, name='RoleAssignmentEdit'),
    path('view/<int:id>', views.View, name='RoleAssignmentView'),
    path('delete/<int:id>', views.Delete, name='RoleAssignmentDelete'),
    path('update-role/<int:id>/', views.UpdateUserPermission, name="UpdateUserPermission"),

    # path('ajax-load-csn/', views.load_company_short_name, name="ajaxLoadCsn")
]
