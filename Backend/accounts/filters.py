import django_filters
from accounts.models import CustomUser

class CustomUserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = {
            "first_name": ["iexact", "icontains"],
            "last_name": ["iexact", "icontains"],
            "email": ["iexact", "icontains"],
        }