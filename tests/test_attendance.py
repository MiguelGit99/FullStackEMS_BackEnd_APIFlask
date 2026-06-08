from types import SimpleNamespace
from unittest.mock import patch


def test_clock_in_success(client, employee_headers):
    fake_attendance = SimpleNamespace(
        employeeId=2,
        date="2026-05-23",
        checkIn="2026-05-23T08:00:00",
        checkOut=None,
        status="Present",
        workingHours=None,
        dayType=None,
    )

    with patch("blueprints.attendance.routes.register_clockIn", return_value=fake_attendance):
        response = client.post("/api/attendance/", headers=employee_headers)

    assert response.status_code == 200
    assert response.get_json()["employeeId"] == 2


def test_get_attendance_success(client, employee_headers):
    attendance_list = [
        SimpleNamespace(
            employeeId=2,
            date="2026-05-23",
            checkIn="2026-05-23T08:00:00",
            checkOut="2026-05-23T17:00:00",
            status="Present",
            workingHours=9,
            dayType="Full Day",
        )
    ]

    with patch("blueprints.attendance.routes.get_all_attendance", return_value=(attendance_list, False)):
        response = client.get("/api/attendance/10", headers=employee_headers)

    assert response.status_code == 200
    assert response.get_json()[0]["employeeId"] == 2


def test_clock_in_requires_token(client):
    response = client.post("/api/attendance/")
    assert response.status_code == 401
