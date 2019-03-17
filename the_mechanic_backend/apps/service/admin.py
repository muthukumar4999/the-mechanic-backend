from django.contrib import admin

# Register your models here.
from the_mechanic_backend.apps.service.models import ServiceType, GeneralService, SubService, Customer, Vehicle, \
    SpareCost, ServiceCost, SubServiceCost, GeneralServiceTestResults, Service


class ServiceTypeAdmin(admin.ModelAdmin):
    model = ServiceType
    list_display = ['service_name', 'is_general', 'has_sub']


class GeneralServiceAdmin(admin.ModelAdmin):
    model = GeneralService
    list_display = ['check_list']


class SubServiceAdmin(admin.ModelAdmin):
    model = SubService
    list_display = ['service', 'sub_service_name']


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ['customer_name', 'customer_phone_number', 'customer_email', 'customer_area']


class VehicleAdmin(admin.ModelAdmin):
    model = Vehicle
    list_display = ['vehicle_number', 'vehicle_brand', 'vehicle_model', 'vehicle_color']


class ServiceAdmin(admin.ModelAdmin):
    model = Service
    list_display = ['customer', 'vehicle', 'status', 'service_in_date', 'delivery_date']


class GeneralServiceTestResultsAdmin(admin.ModelAdmin):
    model = GeneralServiceTestResults
    list_display = ['service', 'check_list', 'status']


class SubServiceCostAdmin(admin.ModelAdmin):
    model = SubServiceCost
    list_display = ['service', 'sub_service', 'cost']


class ServiceCostAdmin(admin.ModelAdmin):
    model = ServiceCost
    list_display = ['service', 'cost']


class SpareCostAdmin(admin.ModelAdmin):
    model = SpareCost
    list_display = ['spare', 'quantity', 'per_price']


admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(GeneralService, GeneralServiceAdmin)
admin.site.register(SubService, SubServiceAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(GeneralServiceTestResults, GeneralServiceTestResultsAdmin)
admin.site.register(SubServiceCost, SubServiceCostAdmin)
admin.site.register(ServiceCost, ServiceCostAdmin)
admin.site.register(SpareCost, SpareCostAdmin)
