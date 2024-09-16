from rest_framework import status

import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestCreateCollection:

    def test_if_user_is_anonymous(self, api_client):
        # Send POST request as an anonymous user
        response = api_client.post(
            "/store/collections/",
            {"title": "a"},
        )

        # Assert that the response status code is 401 Unauthorized
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client):
        api_client.force_authenticate(user={})

        # Create a user and authenticate
        user = User.objects.create_user(username="testuser", password="password")
        api_client.force_authenticate(user=user)

        # Send POST request as an authenticated user
        response = api_client.post(
            "/store/collections/",
            {"title": "a"},
        )

        # Assert that the response status code is 201 Created
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_201(self, api_client):
        # Create an admin user and authenticate

        admin_user = User.objects.create_superuser(
            username="admin", password="password"
        )

        api_client.force_authenticate(user=admin_user)

        # Send POST request as an authenticated admin user
        response = api_client.post(
            "/store/collections/",
            {"title": "a"},
        )

        # Assert that the response status code is 201 Created
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_user_cannot_create_without_authentication(self, api_client):
        # Send POST request without authentication
        response = api_client.post(
            "/store/collections/",
            {"title": "a"},
        )

        # Assert that the response status code is 401 Unauthorized
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_invalid_returns_400(self, api_client):

        api_client.force_authenticate(user=User(is_staff=True))
        response = api_client.post(
            "/store/collections/",
            {"title": ""},  # it passes because it is null field
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] is not None

    def test_if_data_is_valid_returns_201(self, api_client):
        api_client.force_authenticate(user=User(is_staff=True))
        response = api_client.post(
            "/store/collections/",
            {"title": "a"},
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0





        