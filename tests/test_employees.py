from types import SimpleNamespace
from unittest.mock import patch


def test_list_employees(client, admin_headers):
    fake_employees = [
        SimpleNamespace(
            id=1,
            firstName="John",
            lastName="Doe",
            email="john@example.com",
            phone="1234567890",
            position="Developer",
            basicSalary=1000,
            allowances=100,
            deductions=50,
            employmentStatus="ACTIVE",
            joinDate="2026-05-01",
            bio="Bio",
            department="Sales",
            user=SimpleNamespace(id=10, email="john@example.com", role="EMPLOYEE"),
        )
    ]

    with patch("blueprints.employees.routes.get_all_employees", return_value=fake_employees):
        response = client.get("/api/employees/", headers=admin_headers)

    assert response.status_code == 200
    payload = response.get_json()
    assert payload[0]["email"] == "john@example.com"
    assert payload[0]["user"]["role"] == "EMPLOYEE"


def test_list_employees_by_department(client, admin_headers):
    fake_employees = [SimpleNamespace(id=2, firstName="Ana", lastName="Lopez", email="ana@example.com", phone="1234567890", position="Tester", basicSalary=950, allowances=80, deductions=20, employmentStatus="ACTIVE", joinDate="2026-05-01", bio="Bio", department="Human Resources", user=SimpleNamespace(id=11, email="ana@example.com", role="EMPLOYEE"))]

    with patch("blueprints.employees.routes.get_all_employees", return_value=fake_employees):
        response = client.get("/api/employees/Human%20Resources", headers=admin_headers)

    assert response.status_code == 200
    assert response.get_json()[0]["department"] == "Human Resources"


def test_get_employee_by_id(client, admin_headers):
    fake_employee = SimpleNamespace(
        id=1,
        firstName="John",
        lastName="Doe",
        email="john@example.com",
        phone="1234567890",
        position="Developer",
        basicSalary=1000,
        allowances=100,
        deductions=50,
        employmentStatus="ACTIVE",
        joinDate="2026-05-01",
        bio="Bio",
        department="Sales",
        user=SimpleNamespace(id=10, email="john@example.com", role="EMPLOYEE"),
    )

    with patch("blueprints.employees.routes.get_employee", return_value=fake_employee):
        response = client.get("/api/employees/1", headers=admin_headers)

    assert response.status_code == 200
    assert response.get_json()["id"] == 1
    assert response.get_json()["email"] == "john@example.com"


def test_add_employee_success(client, admin_headers):
    fake_employee = SimpleNamespace(
        id=1,
        firstName="New",
        lastName="User",
        email="new@example.com",
        phone="1234567890",
        position="Developer",
        basicSalary=1000,
        allowances=50,
        deductions=20,
        employmentStatus="ACTIVE",
        joinDate="2026-05-01",
        bio="Bio",
        department="Sales",
        user=SimpleNamespace(id=12, email="new@example.com", role="EMPLOYEE"),
    )

    with patch("blueprints.employees.routes.create_employee", return_value=fake_employee):
        response = client.post(
            "/api/employees/",
            headers=admin_headers,
            json={
                "firstName": "New",
                "lastName": "User",
                "email": "new@example.com",
                "phone": "1234567890",
                "position": "Developer",
                "basicSalary": 1000,
                "allowances": 50,
                "deductions": 20,
                "employmentStatus": "ACTIVE",
                "joinDate": "2026-05-01",
                "bio": "Bio",
                "department": "Sales",
                "user": {"email": "new@example.com", "role": "EMPLOYEE", "password": "secret"},
            },
        )

    assert response.status_code == 201
    assert response.get_json()["email"] == "new@example.com"


def test_add_employee_validation_error(client, admin_headers):
    response = client.post(
        "/api/employees/",
        headers=admin_headers,
        json={
            "firstName": "",
            "lastName": "",
            "email": "not-an-email",
        },
    )

    assert response.status_code in (400, 422)
    assert response.get_json()["status"] == "error"


def test_edit_employee_success(client, admin_headers):
    updated_employee = SimpleNamespace(
        id=1,
        firstName="John",
        lastName="Doe",
        email="john@example.com",
        phone="1234567890",
        position="Developer",
        basicSalary=1000,
        allowances=100,
        deductions=50,
        employmentStatus="ACTIVE",
        joinDate="2026-05-01",
        bio="Bio",
        department="Sales",
        user=SimpleNamespace(id=10, email="john@example.com", role="EMPLOYEE"),
    )

    with patch("blueprints.employees.routes.update_employee", return_value=updated_employee):
        response = client.patch(
            "/api/employees/",
            headers=admin_headers,
            json={
                "id": 1,
                "firstName": "John",
                "lastName": "Doe",
                "email": "john@example.com",
            },
        )

    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_delete_employee_success(client, admin_headers):
    with patch("blueprints.employees.routes.soft_delete_employee") as delete_employee:
        response = client.delete("/api/employees/1", headers=admin_headers)

    delete_employee.assert_called_once_with(1)
    assert response.status_code == 204
