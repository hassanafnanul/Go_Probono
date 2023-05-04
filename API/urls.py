from django.urls import path, include
# from API.CategoryAPI import views as CatViews
# from API.OfferAPI import views as OfferViews
# from API.ItemAPI import views as ItemViews
# from API.StoreAPI import views as StoreView
# from API.OrderAPI import views as OrderViews
# from API.UserAPI import  views as UserViews
from API import views

urlpatterns = [

    path('auth/',include('API.UserAPI.urls')),

    path('law/',include('API.Law.urls')),

    path('kyl/',include('API.KnowYourLaw.urls')),

    path('home/',include('API.Home.urls')),

    path('help-center/',include('API.HelpCenter.urls')),

    path('event/',include('API.Event.urls')),
    
    path('team/',include('API.TeamMember.urls')),

    path('lawyer/',include('API.Lawyer.urls')),

    path('global-search/',include('API.GlobalSearch.urls')),

    path('address/',include('API.Address.urls')),
    
    path('appointment/',include('API.Appointment.urls')),

]

