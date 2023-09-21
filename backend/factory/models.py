from django.utils.translation import gettext_lazy as _
from django.db import models
#from user.models import Users
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Factory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
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
    member = models.OneToOneField(to=User, primary_key=True, on_delete=models.CASCADE)
    factory = models.ManyToManyField(Factory, blank=True, default=[])
    product_line = models.ManyToManyField(to=ProductLine, blank=True, default=[], db_constraint=False)
    STATUS = (
        ('ENABLED', 'ENABLED'),
        ('DISABLED', 'DISABLED')
    )
    status = models.CharField(max_length=10, choices=STATUS, default='ENABLED')

    def factories(self):
        return "\n".join([p.name for p in self.factory.all()])

    def product_lines(self):
        return "\n".join([p.name for p in self.product_line.all()])

    @receiver(post_save, sender=User)  # create Users instance after creation of django User.
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            n_user = FactoryMember.objects.create(member=instance)
            n_user.save()

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
