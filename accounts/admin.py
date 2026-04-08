from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile


# ── Restore default User admin (no inline) ──
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'date_joined']


# ── Subscription tab ──
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_vip', 'vip_is_active', 'vip_expires_on']
    list_filter = ['is_vip']
    search_fields = ['user__username', 'user__email']
    fields = [
        'user',
        'is_vip',
        ('vip_activated_on', 'vip_expires_on'),
        'phone',
    ]

    def vip_is_active(self, obj):
        return '✅ Active' if obj.vip_is_active else '❌ Inactive'
    vip_is_active.short_description = 'Status'