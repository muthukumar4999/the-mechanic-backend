from django.conf.urls import url
from django.urls import path

from the_mechanic_backend.v0.accounts import views

urlpatterns = [

    path('login/', views.LoginView.as_view(), name='login'),

    path('user/', views.UserList.as_view(), name='user-list'),

    path('store/', views.StoreList.as_view(), name='store-list'),

    url('file-upload/', views.XlsFileUpload.as_view(), name='file_upload'),

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
