from django.db import models


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
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    brand_model = models.ForeignKey(BrandModel, on_delete=models.CASCADE)
    spare_name = models.CharField(max_length=200)
    spare_local_name = models.CharField(max_length=200, null=True)
    spare_id = models.CharField(max_length=200)
    quantity = models.IntegerField()
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    wholesaler_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mechanic_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    customer_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mrp_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    suppliers = models.CharField(max_length=200)
    quality_class = models.CharField(max_length=100)

    def __str__(self):
        return self.spare_name

    class Meta:
        ordering = ['spare_name']
