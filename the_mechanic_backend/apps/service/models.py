from django.db import models

from the_mechanic_backend.apps.accounts.models import User
from the_mechanic_backend.apps.stock.models import Spare


class ServiceType(models.Model):
    service_name = models.CharField(max_length=200)
    is_general = models.BooleanField(default=False)
    has_sub = models.BooleanField(default=False)

    def __str__(self):
        return self.service_name


class GeneralService(models.Model):
    check_list = models.CharField(max_length=200)

    def __str__(self):
        return self.check_list


class SubService(models.Model):
    service = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    sub_service_name = models.CharField(max_length=200)

    def __str__(self):
        return self.sub_service_name


class Customer(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_phone_number = models.CharField(max_length=10)
    customer_email = models.CharField(max_length=200, null=True, blank=True)
    customer_address = models.TextField()
    customer_area = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.customer_name} - {self.customer_phone_number}'


class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=20)
    vehicle_brand = models.ForeignKey('stock.Brand', on_delete=models.CASCADE)
    vehicle_model = models.ForeignKey('stock.BrandModel', on_delete=models.CASCADE)
    vehicle_color = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.vehicle_number}'


class Service(models.Model):
    NEW = 'NEW'
    LIVE = 'LIVE'
    COMPLETED = 'COMPLETED'
    DELIVERED = 'DELIVERED'

    STATUS = ((NEW, NEW),
              (LIVE, LIVE),
              (COMPLETED, COMPLETED),
              (DELIVERED, DELIVERED))

    # customer details
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    helmet = models.BooleanField(default=False)

    # bike details
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    vehicle_odo_reading = models.CharField(max_length=20)

    # type of service
    services = models.ManyToManyField(ServiceType)

    # status
    status = models.CharField(max_length=20, choices=STATUS, default=NEW)

    # spare
    spare_count = models.IntegerField()

    # date
    service_in_date = models.DateTimeField()
    delivery_date = models.DateTimeField()

    # rework
    is_rework = models.BooleanField(default=False)
    rework_count = models.IntegerField(default=0)

    customer_complaint = models.TextField()

    labour = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    labour_charge = models.DecimalField(max_digits=10, decimal_places=2)

    # pickup details
    is_pickup = models.BooleanField(default=False)
    pickup_cost = models.DecimalField(max_digits=10, decimal_places=2)
    pickup_address = models.TextField()
    delivery_address = models.TextField()

    def __str__(self):
        return f'{self.customer} - {self.vehicle}'


class GeneralServiceTestResults(models.Model):
    WORKING = 'WORKING'
    NOT_WORKING = 'NOT_WORKING'
    REPLACE = 'REPLACE'
    STATUS = ((WORKING, WORKING),
              (NOT_WORKING, NOT_WORKING),
              (REPLACE, REPLACE))
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    check_list = models.ForeignKey(GeneralService, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS)

    def __str__(self):
        return f'{self.check_list} - {self.status}'


class SubServiceCost(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    sub_service = models.ForeignKey(SubService, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.sub_service} - {self.cost}'


class ServiceCost(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.service} - {self.cost}'


class SpareCost(models.Model):
    spare = models.ForeignKey(Spare, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    per_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.spare} - {self.quantity} - {self.per_price}'


class CustomerComplaints(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    complain = models.TextField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.service} - {self.complain}'