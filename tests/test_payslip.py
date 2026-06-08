from types import SimpleNamespace
from unittest.mock import patch


def test_add_payslip_success(client, employee_headers):
    fake_payslip = SimpleNamespace(
        id=1,
        employeeId=2,
        month=12,
        year=2026,
        basicSalary=10000,
        allowances=2000,
        deductions=500,
        netSalary=11500,
    )

    with patch("blueprints.payslip.routes.create_payslip", return_value=fake_payslip):
        response = client.post(
            "/api/payslip/",
            headers=employee_headers,
            json={
                "employeeId": 2,
                "month": 12,
                "year": 2026,
                "basicSalary": 10000,
                "allowances": 2000,
                "deductions": 500,
            },
        )

    assert response.status_code == 200
    assert response.get_json()["employeeId"] == 2


def test_get_payslips_success(client, admin_headers):
    fake_payslips = [
        SimpleNamespace(
            id=1,
            employeeId=2,
            month=12,
            year=2026,
            basicSalary=10000,
            allowances=2000,
            deductions=500,
            netSalary=11500,
        )
    ]

    with patch("blueprints.payslip.routes.get_all_payslip", return_value=fake_payslips):
        response = client.get("/api/payslip/", headers=admin_headers)

    assert response.status_code == 200
    assert response.get_json()[0]["month"] == 12


def test_get_payslip_by_id_success(client, employee_headers):
    fake_payslip = SimpleNamespace(
        id=1,
        employeeId=2,
        month=12,
        year=2026,
        basicSalary=10000,
        allowances=2000,
        deductions=500,
        netSalary=11500,
    )

    with patch("blueprints.payslip.routes.get_payslip", return_value=fake_payslip):
        response = client.get("/api/payslip/1", headers=employee_headers)

    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_add_payslip_validation_error(client, employee_headers):
    response = client.post(
        "/api/payslip/",
        headers=employee_headers,
        json={"employeeId": 2, "month": 13, "year": 2026, "basicSalary": -100},
    )

    assert response.status_code in (400, 422)
    assert response.get_json()["status"] == "error"
