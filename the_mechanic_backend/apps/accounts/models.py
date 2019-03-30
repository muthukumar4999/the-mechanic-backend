from django.contrib.auth.models import User
from django.db import models


class AuthUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Store(models.Model):
    SERVICE = 'SERVICE'
    SPARE = 'SPARE'
    STORE_TYPE = ((SERVICE, SERVICE),
                  (SPARE, SPARE))
    name = models.CharField(max_length=200)
    branch = models.CharField(max_length=200)
    type = models.CharField(max_length=200, choices=STORE_TYPE)
    address = models.TextField()


"""
{
"name": "Mr.Mechanic",
"branch":"Palavakam",
"type":"SPARE",
"address":""
}
"""