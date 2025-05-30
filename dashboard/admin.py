from django.contrib import admin

from .models import Profile

@admin.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'birth_date')
    list_display_link = ('user', 'full_name', 'email', 'birth_date')
    search_fields = ('user__username', 'full_name', 'email')
    list_filter = ('birth_date',)
    ordering = ('user__username',)
    fieldsets = (
        (None, {
            'fields': ('user', 'full_name', 'email', 'birth_date')
        }),
    )
