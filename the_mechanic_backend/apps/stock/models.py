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
    FIRST = 'FIRST'
    SECOND = 'SECOND'
    THIRD = 'THIRD'
    CLASS = ((FIRST, FIRST),
             (SECOND, SECOND),
             (THIRD, THIRD))

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    brand_model = models.ForeignKey(BrandModel, on_delete=models.CASCADE)
    spare_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    per_price = models.DecimalField(max_digits=10, decimal_places=2)
    suppliers = models.CharField(max_length=200)
    quality_class = models.CharField(max_length=100, choices=CLASS)

    def __str__(self):
        return self.spare_name

    class Meta:
        ordering = ['spare_name']
