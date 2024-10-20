from django.contrib import admin

from accounts.models import UserAccount


# Register your models here.
@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    search_fields = ('email',)
