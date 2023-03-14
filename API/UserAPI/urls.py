from django.urls import path
from . import views


urlpatterns = [

    #REGISTRATION
    path('register/', views.Register, name='Register'),
    # path('exist/', views.UserExists),

    # #LOGIN
    path('login/', views.UserVerification),

    # #MOBILE OTP
    # path('mobile/verification/', views.MobileVerification),
    # path('mobile/OTP-send/', views.MobileOTPSend),
    # path('mobile/OTP-resend/', views.MobileOTPResend),

    # #EMAIL OTP
    # path('email/validation/', views.EmailValidation),
    # path('email/verification/', views.EmailVerification),
    # path('email/OTP-send/', views.EmailOTPSend),
    # path('email/OTP-resend/', views.EmailOTPResend),

    # #PROFILE
    # # path('profile/<str:token>/', views.CustomerProfile.as_view()),
    path('profile/', views.CustomerProfile.as_view()),

    # #RESET PASSWORD
    # path('update/password/', views.UpdatePassword),

    # #UPDATE PROFILE
    path('update/profile/', views.UpdateProfile)
]