from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import Group


@admin.action(description="Approve selected users")
def approve_users(modeladmin, request, queryset):
    for user in queryset:
        if user.user_type:  # Ensure admin sets user_type
            group, _ = Group.objects.get_or_create(
                name=user.user_type.capitalize() + "s"
            )
            user.groups.add(group)
            user.is_approved = True
            user.save()


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["email", "user_type", "is_approved"]
    list_filter = ["is_approved", "user_type"]
    actions = [approve_users]


admin.site.register(CustomUser, CustomUserAdmin)
