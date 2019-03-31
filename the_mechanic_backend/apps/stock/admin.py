from django.contrib import admin

# Register your models here.
from the_mechanic_backend.apps.stock.models import Brand, BrandModel, Spare, SpareOrder, SpareCustomer, SpareSold


class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ['name', ]


class BrandModelAdmin(admin.ModelAdmin):
    model = BrandModel
    list_display = ['brand', 'model_name']


class SpareAdmin(admin.ModelAdmin):
    model = Spare
    list_display = ['store', 'brand', 'brand_model', 'spare_name', 'spare_local_name', 'quantity', 'buying_price',
                    'mrp_price']


class SpareOrderAdmin(admin.ModelAdmin):
    model = SpareOrder
    list_display = ['order_id', 'customer', 'total']


class SpareCustomerAdmin(admin.ModelAdmin):
    model = SpareCustomer
    list_display = ['name', 'phone_number']


class SpareSoldAdmin(admin.ModelAdmin):
    model = SpareSold
    list_display = ['spare_name', 'order']


admin.site.register(Brand, BrandAdmin)
admin.site.register(BrandModel, BrandModelAdmin)
admin.site.register(Spare, SpareAdmin)
admin.site.register(SpareOrder, SpareOrderAdmin)
admin.site.register(SpareCustomer, SpareCustomerAdmin)
admin.site.register(SpareSold, SpareSoldAdmin)
