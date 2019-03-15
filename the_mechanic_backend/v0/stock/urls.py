from django.urls import path

from the_mechanic_backend.v0.stock import views

urlpatterns = [

    path('brand/', views.BrandList.as_view(), name='brand-list'),

    path('brand/<slug:brand_id>/model/', views.BrandModelList.as_view(), name='brand-model-list'),

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
