from types import SimpleNamespace
from unittest.mock import patch


def test_get_profile_success(client, employee_headers):
    response = client.get("/api/profile/", headers=employee_headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data["email"] == "employee@example.com"
    assert data["role"] == "EMPLOYEE"


def test_edit_profile_success(client, employee_headers):
    with patch("blueprints.profile.routes.update_profile", return_value=SimpleNamespace(id=2, bio="New bio")):
        response = client.post(
            "/api/profile/",
            headers=employee_headers,
            json={"bio": "New bio"},
        )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Profile successfully changed."


def test_edit_profile_validation_error(client, employee_headers):
    response = client.post(
        "/api/profile/",
        headers=employee_headers,
        json={"bio": ""},
    )

    assert response.status_code in (400, 422)
    assert response.get_json()["status"] == "error"
