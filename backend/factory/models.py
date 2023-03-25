from django.utils.translation import gettext_lazy as _
from django.db import models
from user.models import Users


class Factory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    delete = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Shift(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    factory = models.ForeignKey(to=Factory, on_delete=models.CASCADE)
    start_at = models.TimeField(null=True, blank=True)
    ends_at = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    factory = models.ForeignKey(to=Factory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductLinePart(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    product_line = models.ForeignKey(to=ProductLine, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductLinePart2(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    product_line_part = models.ForeignKey(to=ProductLinePart, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class FactoryMember(models.Model):
    member = models.OneToOneField(to=Users, primary_key=True, on_delete=models.CASCADE)
    factory = models.ManyToManyField(Factory, blank=True)
    product_line_id = models.ManyToManyField(to=ProductLine, blank=True)
    STATUS = (
        ('ENABLED', 'ENABLED'),
        ('DISABLED', 'DISABLED')
    )
    status = models.CharField(max_length=10, choices=STATUS, default='ENABLED')

    def factories(self):
        return "\n".join([p.products for p in self.factory.all()])

    def product_lines(self):
        return "\n".join([p.products for p in self.product_line_id.all()])


class SettingsType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    field = models.CharField(max_length=255)
    syntax = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Settings(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    factory = models.ForeignKey(to=Factory, on_delete=models.CASCADE)
    inputs = models.CharField(max_length=255)
    settings_type = models.ForeignKey(to=SettingsType, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
