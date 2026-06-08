from types import SimpleNamespace
from unittest.mock import patch
import pytest


def test_login_success(client):
    user = SimpleNamespace(
        id="1",
        email="admin@example.com",
        role="ADMIN",
        employee=SimpleNamespace(id=1, firstName="Admin", lastName="User"),
    )

    with patch("blueprints.auth.routes.verify_login", return_value=user):
        response = client.post(
            "/api/auth/login",
            json={"email": "admin@example.com", "password": "secret"},
        )

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["data"]["user"]["email"] == "admin@example.com"
    assert data["data"]["isValid"] is True
    assert "access_token" in data["data"]
    assert "access_token_cookie" in response.headers.get("Set-Cookie", "")


def test_login_validation_error(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "invalid-email", "password": ""},
    )

    assert response.status_code in (400, 422)
    assert response.get_json()["status"] == "error"


def test_logout_requires_authorization(client, admin_headers):
    response = client.post("/api/auth/logout", headers=admin_headers)

    assert response.status_code == 200
    assert response.get_json()["message"] == "Session successfully closed."


def test_change_password_success(client, admin_headers):
    with patch("blueprints.auth.routes.update_password") as update_password:
        response = client.post(
            "/api/auth/change_password",
            headers=admin_headers,
            json={"currentPassword": "oldpass", "newPassword": "newpass"},
        )

    assert response.status_code == 200
    update_password.assert_called_once()
    assert response.get_json()["message"] == "Password successfully changed."


def test_change_password_validation_error(client, admin_headers):
    response = client.post(
        "/api/auth/change_password",
        headers=admin_headers,
        json={"currentPassword": "", "newPassword": ""},
    )

    assert response.status_code in (400, 422)
    assert response.get_json()["status"] == "error"


@pytest.mark.xfail(
    reason="El endpoint /api/auth/refresh actualmente construye user_payload como dict y luego intenta acceder a user_payload.user.id",
)
def test_refresh_endpoint_client_side_bug(client, admin_headers):
    response = client.post("/api/auth/refresh", headers=admin_headers)
    assert response.status_code == 200
