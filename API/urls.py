from django.urls import path, include
# from API.CategoryAPI import views as CatViews
# from API.OfferAPI import views as OfferViews
# from API.ItemAPI import views as ItemViews
# from API.StoreAPI import views as StoreView
# from API.OrderAPI import views as OrderViews
# from API.UserAPI import  views as UserViews
from API import views

urlpatterns = [

    # path('categories/',include('API.CategoryAPI.urls')),

    # path('items/',include('API.ItemAPI.urls')),

    # path('offers/',include('API.OfferAPI.urls')),

    # path('orders/',include('API.OrderAPI.urls')),

    # path('stores/', include('API.StoreAPI.urls')),

    path('users/',include('API.UserAPI.urls')),

    path('law/',include('API.Law.urls')),

    # path('brands/',include('API.BrandAPI.urls')),

    # path('request-items/',include('API.RequestItemAPI.urls')),

    # path('search/',include('API.SmartSearchAPI.urls')),

    # path('warranty-claim/',include('API.WarrantyClaimAPI.urls')),
    
    # path('configuration/',include('API.ConfigurationAPI.urls')),
    
    # path('home/',include('API.HomeConfigure.urls')),

    # path('eshop-items/',include('API.EshopItemsApi.urls')),

    # path('eshop-order/',include('API.EshopOrderAPI.urls')),

    # path('eshop-zone/',include('API.EshopDeliveryZoneAPI.urls')),
    
    # path('eshop-offers/',include('API.EshopOfferAPI.urls')),
    
    # path('external-code/',include('API.ExternalCode.urls')),
    
    # path('voucher/', views.check_voucher_exists.as_view(), name='check_voucher_exists'),
    
    # path('url-type/<str:url>/', views.findUrlType, name='findUrlType'),

]

