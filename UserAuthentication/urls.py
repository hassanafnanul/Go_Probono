from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.UserAuthManagement, name='UserAuth'),
    path('login/', views.loginview, name="loginpage"),
    path('logout/',views.logout_view ,name='logout'),
    path('home/', views.gohome, name="gohome"),
    # path('profile/', views.UpdateProfile, name="userprofile"),

    # path('home/<int:id>/', views.demo_home, name='orderNoteDone')
]
