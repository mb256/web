from django.contrib import admin
from .models import ClubInfo, PictureOfWeek


@admin.register(ClubInfo)
class ClubInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'founded_year', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'founded_year', 'location')
        }),
        ('Contact', {
            'fields': ('email', 'phone')
        }),
        ('Content', {
            'fields': ('description', 'history')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance (singleton)
        return not ClubInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of club info
        return False


@admin.register(PictureOfWeek)
class PictureOfWeekAdmin(admin.ModelAdmin):
    list_display = ['caption', 'photographer', 'date_added', 'is_active']
    list_filter = ['is_active', 'date_added']
    search_fields = ['caption', 'photographer']
    readonly_fields = ['date_added']
    
    fieldsets = (
        (None, {
            'fields': ('image', 'caption', 'photographer', 'is_active')
        }),
        ('Metadata', {
            'fields': ('date_added',),
            'classes': ('collapse',)
        }),
    )
