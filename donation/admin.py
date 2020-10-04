from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Donation, Category, Institution

#
class CustomUserAdmin(UserAdmin):
    # model = CustomUser
    # list_display = ('email', 'is_staff', 'is_active',)
    # list_filter = ('email', 'is_staff', 'is_active',)
    # fieldsets = (
    #     (None, {'fields': ('email', 'password')}),
    #     ('Permissions', {'fields': ('is_staff', 'is_active')}),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
    #     ),
    # )
    search_fields = ('email',)
    ordering = ('email',)

# admin.site.register(CustomUser)
admin.site.register(Institution)
admin.site.register(Category)
admin.site.register(Donation)
# admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)