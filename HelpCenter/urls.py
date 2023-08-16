from django.urls import path
from . import views, ch_views

urlpatterns = [
    path('', views.RulesManagement, name='RulesManagement'),
    # path('create/', views.RulesCreate, name='RulesCreate'),
    path('edit/<int:id>/', views.RulesEdit, name='RulesEdit'),
    path('view/<int:id>/', views.RulesView, name='RulesView'),

    
    path('call-history/', ch_views.CallHistoryManagement, name='CallHistoryManagement'),
    path('call-history/create/', ch_views.CallHistoryCreate, name='CallHistoryCreate'),
    # path('call-history/edit/<int:id>/', ch_views.CallHistoryEdit, name='CallHistoryEdit'),
    path('call-history/view/<int:id>/', ch_views.CallHistoryView, name='CallHistoryView'),

]
