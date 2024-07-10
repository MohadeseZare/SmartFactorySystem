from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


# class OperationsTypes(models.Model):
#     id = models.AutoField(primary_key=True)
#     type = models.CharField(max_length=100)
#     name = models.CharField(max_length=150)
#
#
# class Permissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=250)
#     object = models.CharField(max_length=100)  # that use for details
#     created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
#     update_at = models.DateTimeField(null=True, blank=True, auto_now=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#
#     def __str__(self):
#         return self.name
#
#
# class Roles(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     is_predefined = models.BooleanField()
#     description = models.CharField(max_length=255)
#     created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
#     update_at = models.DateTimeField(null=True, blank=True, auto_now=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#
#     def __str__(self):
#         return self.name
#
#
# class PermissionsRole(models.Model):
#     role_id = models.ForeignKey(to=Roles, on_delete=models.CASCADE, )
#     permissions_id = models.ForeignKey(to=Permissions, on_delete=models.CASCADE)
#     operation_type_id = models.ForeignKey(to=OperationsTypes, on_delete=models.CASCADE)


class Users(models.Model):
    username = models.OneToOneField(User, models.CASCADE, default=1)
    first_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=60, null=True)
    email = models.EmailField(max_length=254, unique=True, null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    phone_number = models.CharField(max_length=30, null=True)

    # GENDER = (
    #     ('male', 'male'),
    #     ('female', 'female')
    # )
    # gender = models.CharField(max_length=7, choices=GENDER, null=True)
    # city = models.CharField(max_length=100, null=True)
    # address = models.CharField(max_length=255, null=True)
    # deleted_at = models.DateTimeField(null=True, blank=True)
    # updated_at = models.DateTimeField(null=True, auto_now=True)
    def __str__(self):
        return f"{self.username}"

    @receiver(post_save, sender=User)  # create Users instance after creation of django User.
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            n_user = Users.objects.create(username=instance)
            n_user.save()