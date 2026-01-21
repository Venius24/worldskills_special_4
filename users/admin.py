from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address, SecurityQuestion

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_subscribed', 'preferred_delivery']
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('phone', 'profile_image', 'is_subscribed', 'preferred_delivery', 
                      'security_question', 'security_answer')
        }),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'label', 'city', 'is_preferred']
    list_filter = ['is_preferred', 'city']

@admin.register(SecurityQuestion)
class SecurityQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'is_active']
    list_filter = ['is_active']