from django.contrib import admin

# Register your models here.
from the_mechanic_backend.apps.stock.models import Brand, BrandModel, Spare


class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ['name', ]


class BrandModelAdmin(admin.ModelAdmin):
    model = BrandModel
    list_display = ['brand', 'model_name']


class SpareAdmin(admin.ModelAdmin):
    model = Spare
    list_display = ['store', 'brand', 'brand_model', 'spare_name', 'spare_local_name', 'quantity', 'buying_price', 'mrp_price']


admin.site.register(Brand, BrandAdmin)
admin.site.register(BrandModel, BrandModelAdmin)
admin.site.register(Spare, SpareAdmin)
