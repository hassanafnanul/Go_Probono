from django.urls import path
from . import views

urlpatterns=[
    path('',views.TeamManagement,name='TeamManagement'),
    path('add/',views.TeamAdd,name='TeamAdd'),
    path('view/<int:id>/',views.TeamView,name='TeamView'),
    path('edit/<int:id>/',views.TeamEdit,name='TeamEdit'),


    # path('send-email/',views.SendEmail,name='SendEmail')
]
