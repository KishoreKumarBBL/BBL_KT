from django.contrib import admin
from .models import AnimeUser,UserProfile
 
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'firstname', 'lastname', 'is_active', 'is_staff', 'is_superadmin')
    list_filter = ('is_active', 'is_staff', 'is_superadmin')
    search_fields = ('email', 'username', 'firstname', 'lastname')
    ordering = ('email',)
 
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'created_at', 'updated_at')
    search_fields = ('user__email', 'user__username', 'bio')
 
# Register your models
admin.site.register(AnimeUser, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)