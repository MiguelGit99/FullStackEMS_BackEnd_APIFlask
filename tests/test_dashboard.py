from types import SimpleNamespace
from unittest.mock import patch


def test_get_dashboard_admin_view(client, admin_headers):
    admin_body = {
        "admin_view": {
            "role": "ADMIN",
            "totalEmployees": 10,
            "totalDepartments": 3,
            "totalAttendance": 5,
            "pendingLeaves": 2,
        }
    }

    with patch("blueprints.dashboard.routes.get_all_dashboard", return_value=admin_body):
        response = client.get("/api/dashboard/", headers=admin_headers)

    assert response.status_code == 200
    assert response.get_json()["admin_view"]["role"] == "ADMIN"


def test_get_dashboard_employee_view(client, employee_headers):
    employee_body = {
        "employee_view": {
            "role": "EMPLOYEE",
            "employeeId": 2,
            "employee": {
                "id": 2,
                "firstName": "Employee",
                "lastName": "User",
                "email": "employee@example.com",
                "user": {"id": 2, "email": "employee@example.com", "role": "EMPLOYEE"},
            },
            "currentMonthAttendance": 4,
            "pendingLeaves": 1,
            "latestPayslip": None,
        }
    }

    with patch("blueprints.dashboard.routes.get_all_dashboard", return_value=employee_body):
        response = client.get("/api/dashboard/", headers=employee_headers)

    assert response.status_code == 200
    assert response.get_json()["employee_view"]["employeeId"] == 2
