from types import SimpleNamespace
from unittest.mock import patch


def test_create_leave_success(client, employee_headers):
    fake_leave = SimpleNamespace(
        employeeId=2,
        type="Annual",
        startDate="2026-12-01",
        endDate="2026-12-05",
        reason="Vacation time",
        status="Pending",
    )

    with patch("blueprints.leave_application.routes.add_leave", return_value=fake_leave):
        response = client.post(
            "/api/leave_application/",
            headers=employee_headers,
            json={
                "employeeId": 2,
                "type": "Annual",
                "startDate": "2026-12-01",
                "endDate": "2026-12-05",
                "reason": "Vacation time",
            },
        )

    assert response.status_code == 201
    assert response.get_json()["employeeId"] == 2


def test_create_leave_validation_error(client, employee_headers):
    response = client.post(
        "/api/leave_application/",
        headers=employee_headers,
        json={
            "employeeId": 2,
            "type": "VACATION",
            "startDate": "2020-01-01",
            "endDate": "2020-01-02",
            "reason": "",
        },
    )

    assert response.status_code in (400, 422)
    assert response.get_json()["status"] == "error"


def test_get_leaves_success(client, admin_headers):
    fake_leaves = [
        SimpleNamespace(
            employeeId=2,
            type="Annual",
            startDate="2026-12-01",
            endDate="2026-12-05",
            reason="Vacation time",
            status="Pending",
        )
    ]

    with patch("blueprints.leave_application.routes.get_all_leaves", return_value=fake_leaves):
        response = client.get(
            "/api/leave_application/?status=Pending",
            headers=admin_headers,
        )

    assert response.status_code == 200
    assert response.get_json()[0]["status"] == "Pending"


def test_edit_leave_status_success(client, admin_headers):
    updated_leave = SimpleNamespace(
        employeeId=2,
        type="Annual",
        startDate="2026-12-01",
        endDate="2026-12-05",
        reason="Vacation time",
        status="Approved",
    )

    with patch("blueprints.leave_application.routes.update_leave_status", return_value=updated_leave):
        response = client.patch(
            "/api/leave_application/",
            headers=admin_headers,
            json={
                "employeeId": 2,
                "status": "Approved",
            },
        )

    assert response.status_code == 200
    assert response.get_json()["status"] == "Approved"
