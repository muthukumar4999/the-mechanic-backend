from django.contrib import admin

# Register your models here.
from the_mechanic_backend.apps.stock.models import Brand, BrandModel, Spares


class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ['name', ]


class BrandModelAdmin(admin.ModelAdmin):
    model = BrandModel
    list_display = ['brand', 'model_name']


class SparesAdmin(admin.ModelAdmin):
    model = Spares
    list_display = ['brand', 'brand_model', 'spare_name', 'quantity', 'per_price']


admin.site.register(Brand, BrandAdmin)
admin.site.register(BrandModel, BrandModelAdmin)
admin.site.register(Spares, SparesAdmin)
