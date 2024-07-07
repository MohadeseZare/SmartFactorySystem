from django.db import models
from user.models import Users
from factory.models import ProductLine


class Alarms(models.Model):
    id = models.BigAutoField(primary_key=True)
    data = models.CharField(max_length=500)
    user = models.ManyToManyField(Users)
    time = models.DateTimeField()
    productLine = models.ForeignKey(ProductLine, on_delete=models.CASCADE)

