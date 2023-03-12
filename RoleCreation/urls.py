from django.urls import path
from . import views

urlpatterns = [
    path('',views.RoleManagement,name='RoleManagement'),
    path('add/',views.RoleCreate,name='RoleCreate'),
    path('view/<int:id>/',views.RoleView,name='RoleView'),
    path('edit/<int:id>/',views.RoleEdit,name='RoleEdit')
    
]
