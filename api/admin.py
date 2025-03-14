from django.contrib import admin
from api.models import User,Profile

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name']

admin.site.register(User)
admin.site.register( Profile)