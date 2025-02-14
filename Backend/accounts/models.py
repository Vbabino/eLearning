from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group


# Create your models here.

USER_TYPES = [("student", "Student"), ("teacher", "Teacher")]


class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser model where email is the unique identifier"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        user.assign_user_group()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model where email is the unique identifier instead of username"""

    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
    )

    objects = CustomUserManager()

    def assign_user_group(user): 
        """Assign user to a group based on user_type"""
        if user.user_type == "student":
            group, _ = Group.objects.get_or_create(name="Students")
        elif user.user_type == "teacher":
            group, _ = Group.objects.get_or_create(name="Teachers")
        else:
            return

        user.groups.add(group)


class StatusUpdate(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="status_updates"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
