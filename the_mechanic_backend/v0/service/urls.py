from django.urls import path

from the_mechanic_backend.v0.service import views

urlpatterns = [
    path('', views.ServiceList.as_view(), name='create-service'),
    #
    # path('<int:service_id>/', views.ServiceDetailsView.as_view(), name='update-service'),

    path('general/', views.GeneralServiceView.as_view(), name='general-service'),

    path('service_type/', views.ServiceTypeView.as_view(), name='sub-service'),

    path('service_type/<int:service_type_id>/sub_service', views.SubServiceView.as_view(), name='sub-service'),




]
