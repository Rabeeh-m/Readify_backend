from django.contrib import admin
from api.models import User,Profile,Book,ReadingList,ReadingListItem

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name']

admin.site.register(User)
admin.site.register( Profile)
admin.site.register( Book)
admin.site.register( ReadingList)
admin.site.register( ReadingListItem)