from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('theadmin/', admin.site.urls),

    path('', include('UserAuthentication.urls')),

    path('userauth/', include('UserAuthentication.urls')),

    path('module-task/', include('ModuleManagement.urls')),

    path('audit/',include('LogWithAudit.urls')),

    path('rolemanagement/',include('RoleCreation.urls')),

    path('usermanagement/',include('RoleAssignment.urls')),

]
