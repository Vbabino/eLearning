import pytest
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async

User = get_user_model()


@pytest.fixture
@pytest.mark.django_db(transaction=True)
async def test_user():
    """Fixture to create and return a test user with a valid JWT token."""
    user = await database_sync_to_async(User.objects.create_user)(
        email="testuser10@email.com", password="testuser10"
    )
    access_token = str(AccessToken.for_user(user))
    return user, access_token
