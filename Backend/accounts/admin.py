from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import Group
from accounts.utils import send_approval_email

@admin.action(description="Approve selected users")
def approve_users(modeladmin, request, queryset):
    for user in queryset:
        if user.user_type:  
            group, _ = Group.objects.get_or_create(
                name=user.user_type.capitalize() + "s"
            )
            user.groups.add(group)
            user.is_approved = True
            user.save()
            send_approval_email(user)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["email", "user_type", "is_approved"]
    list_filter = ["is_approved", "user_type"]
    actions = [approve_users]


admin.site.register(CustomUser, CustomUserAdmin)
