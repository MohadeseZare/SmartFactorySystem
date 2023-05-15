from django.contrib import admin


# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number')
