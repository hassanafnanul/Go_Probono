from django.urls import path
from . import views

urlpatterns = [
    path('', views.RegularPageManagement, name='RegularPage'),
    # path('create/', views.RulesCreate, name='RulesCreate'),
    path('edit/<int:id>/', views.RegularPageEdit, name='RegularPageEdit'),
    path('view/<int:id>/', views.RegularPageView, name='RegularPageView'),

]
