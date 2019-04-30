from django.db import models

from the_mechanic_backend.apps.accounts.models import Store, User


class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class BrandModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=200)

    def __str__(self):
        return self.model_name

    class Meta:
        ordering = ['model_name']


class Spare(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    brand_model = models.ForeignKey(BrandModel, on_delete=models.CASCADE)
    spare_name = models.CharField(max_length=200)
    spare_local_name = models.CharField(max_length=200, null=True)
    spare_id = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField()
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    wholesaler_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mechanic_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    customer_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mrp_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    suppliers = models.CharField(max_length=200)
    quality_class = models.CharField(max_length=100)
    is_urgent_spare = models.BooleanField(default=False)
    spare_location = models.CharField(max_length=500, default="", null=True, blank=True)

    def __str__(self):
        return self.spare_name

    class Meta:
        ordering = ['spare_name']


class SpareCustomer(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    address = models.TextField()

    def __str__(self):
        return self.name


class SpareOrder(models.Model):
    IN_SOURCE = 'IN_SOURCE'
    OUT_SOURCE = 'OUT_SOURCE'
    TYPE = ((IN_SOURCE, IN_SOURCE),
            (OUT_SOURCE, OUT_SOURCE))
    order_id = models.CharField(max_length=20)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=20, choices=TYPE)
    bike_number = models.CharField(max_length=20, default="")
    labour_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    out_source_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    customer = models.ForeignKey(SpareCustomer, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    sold_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id


class SpareSold(models.Model):
    MRP = 'MRP'
    MECHANIC = 'MECHANIC'
    WHOLESALER = 'WHOLESALER'
    CUSTOMER = 'CUSTOMER'
    price_type = ((MRP, MRP),
                  (MECHANIC, MECHANIC),
                  (WHOLESALER, WHOLESALER),
                  (CUSTOMER, CUSTOMER))
    order = models.ForeignKey(SpareOrder, on_delete=models.CASCADE)
    spare = models.ForeignKey(Spare, on_delete=models.SET('deleted'))
    spare_count = models.IntegerField()
    spare_name = models.CharField(max_length=100)
    spare_buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    spare_price = models.DecimalField(max_digits=10, decimal_places=2)
    spare_price_type = models.CharField(max_length=20, choices=price_type)
