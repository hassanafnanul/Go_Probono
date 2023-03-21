from django.contrib import admin
from django.urls import path, include
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('theadmin/', admin.site.urls),

    path('api/',include('API.urls')),

    path('', include('UserAuthentication.urls')),

    path('userauth/', include('UserAuthentication.urls')),

    path('module-task/', include('ModuleManagement.urls')),

    path('audit/',include('LogWithAudit.urls')),

    path('rolemanagement/',include('RoleCreation.urls')),

    path('usermanagement/',include('RoleAssignment.urls')),

    path('customer/',include('Customer.urls')),

    path('law/', include('LawManagement.urls')),

    path('slider/', include('SliderManagement.urls')),
    
    path('ckeditor/', include('Go_Probono.ck_editor_uploader_urls')),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                    path('debug/', include(debug_toolbar.urls)),
                  ] + urlpatterns

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

