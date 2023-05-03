from django.urls import path
from . import views

urlpatterns=[
    path('',views.EventManagement,name='EventManagement'),
    path('add/',views.EventAdd,name='EventAdd'),
    path('view/<int:id>/',views.EventView,name='EventView'),
    path('edit/<int:id>/',views.EventEdit,name='EventEdit'),


    # path('send-email/',views.SendEmail,name='SendEmail')
]
