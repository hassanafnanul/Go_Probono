from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('theadmin/', admin.site.urls),

    path('', include('UserAuthentication.urls')),

    

]
