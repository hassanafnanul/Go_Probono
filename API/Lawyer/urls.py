from django.urls import path
from . import views

urlpatterns = [
    path('', views.LawyerAPI.as_view(), name='LawyerAPI'),
    path('<int:id>/', views.LawyerDetailsAPI.as_view(), name='LawyerDetailsAPI'),
    path('categories/', views.LawyerCategoriesAPI.as_view(), name='LawyerCategoriesAPI'),
]