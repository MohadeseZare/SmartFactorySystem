from django.db import models
from factory.models import ProductLinePart


class DeviceType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=50)  # the mac_address have 16 bit or 32 bit
    port = models.CharField(max_length=10)
    position = models.IntegerField()
    data = models.CharField(max_length=1050)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    product_line_part = models.ForeignKey(to=ProductLinePart, on_delete=models.CASCADE)
    device_type = models.ForeignKey(to=DeviceType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class HistoryData(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_id = models.ForeignKey(to=Device, on_delete=models.CASCADE)
    data = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    # data can be numeric or character and add the time one and just one filed for them


class LineDevice(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=50)  # the mac_address have 16 bit or 32 bit
    port = models.CharField(max_length=10, default="")
    position = models.IntegerField(default="")
    data = models.CharField(max_length=1050, default="")
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)


class ErrorLine(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.IntegerField()
    is_vital = models.BooleanField(default=False)
    SECTION = (
        ('stacker', 'stacker'),
        ('packaging machine', 'packaging machine')
    )
    section = models.CharField(max_length=20, choices=SECTION)
    description = models.CharField(max_length=200)
