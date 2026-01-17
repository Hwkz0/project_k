"""Tests for user endpoints."""

import pytest
from fastapi import status


class TestUserEndpoints:
    """Test user endpoints."""

    def test_get_current_user(self, client, auth_headers):
        """Test getting current user profile."""
        response = client.get("/api/v1/users/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"

    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without auth fails."""
        response = client.get("/api/v1/users/me")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_current_user(self, client, auth_headers):
        """Test updating current user profile."""
        response = client.put(
            "/api/v1/users/me",
            headers=auth_headers,
            json={
                "full_name": "Updated Name",
                "bio": "This is my bio",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["full_name"] == "Updated Name"
        assert data["bio"] == "This is my bio"

    def test_get_user_by_id(self, client, test_user):
        """Test getting a user's public profile."""
        response = client.get(f"/api/v1/users/{test_user.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "testuser"
        # Public profile shouldn't include email
        assert "email" not in data or data.get("email") is None

    def test_get_nonexistent_user(self, client):
        """Test getting non-existent user fails."""
        response = client.get("/api/v1/users/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
