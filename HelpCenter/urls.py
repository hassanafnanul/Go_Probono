from django.urls import path
from . import views

urlpatterns = [
    path('', views.RulesManagement, name='RulesManagement'),
    # path('create/', views.RulesCreate, name='RulesCreate'),
    path('edit/<int:id>/', views.RulesEdit, name='RulesEdit'),
    path('view/<int:id>/', views.RulesView, name='RulesView'),

]
