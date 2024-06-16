from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'usercode', 'is_admin', 'is_approved')
    list_filter = ('is_admin', 'is_approved')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'usercode')}),
        ('Permissions', {'fields': ('is_admin', 'is_approved')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'usercode', 'name', 'password1', 'password2', 'is_admin', 'is_approved'),
        }),
    )
    search_fields = ('email', 'usercode', 'name')
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)
