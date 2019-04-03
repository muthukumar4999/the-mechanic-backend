from django.urls import path

from the_mechanic_backend.v0.stock import views

urlpatterns = [

    path('brand/', views.BrandList.as_view(), name='brand-list'),

    path('brand/<int:brand_id>/model/', views.BrandModelList.as_view(), name='brand-model-list'),

    path('<int:store_id>/model/<int:brand_model_id>/spare/', views.SpareList.as_view(), name='model-spare-list'),

    path('spare/<int:store_id>/search/', views.SpareSearchList.as_view(), name='global-spare-search'),

    path('spare/<int:spare_id>/', views.SpareDetails.as_view(), name='model-spare-details'),

    path('<int:store_id>/spare/order/', views.SpareOrderList.as_view(), name='spare-order-list'),

    path('<int:store_id>/spare/urgent/', views.UrgentSpareList.as_view(), name='spare-urgent-list'),

    path('spare/order/<order_id>/email/', views.SpareOrderEmailPdf.as_view(), name='spare-order-email'),

    path('spare/accounting/', views.SparesAccountingView.as_view(), name='spare-order-list'),

    # path('users/', views.UserList.as_view(), name='user-list'),
    #
    # path('login/', views.LoginView.as_view(), name='login'),
    #
    # path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    #
    # path('create-password/<slug:token>/', views.CreatePasswordView.as_view(), name='create-password'),
    #
    # path('change-password/<slug:token>/', views.ChangePasswordView.as_view(), name='change-password'),
    #
    # path('reset-password/', views.ChangePasswordView.as_view(), name='reset-password'),
    #
    # path('user-check/',views.UserExists.as_view(), name='user-check'),
]