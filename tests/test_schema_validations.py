import pytest
from pydantic import ValidationError
from blueprints.auth.schemas import ChangePasswordSchema, LoginSchema
from blueprints.employees.schemas import EmployeeCreateSchema
from blueprints.leave_application.schemas import LeaveApplicationSchema
from blueprints.payslip.schemas import PayslipSchema
from blueprints.profile.schemas import ProfileSchema


def test_login_schema_requires_password():
    with pytest.raises(ValidationError):
        LoginSchema(email="admin@example.com", password="")


def test_change_password_schema_requires_fields():
    with pytest.raises(ValidationError):
        ChangePasswordSchema(currentPassword="", newPassword="")


def test_employee_schema_validates_phone_and_salary():
    with pytest.raises(ValidationError):
        EmployeeCreateSchema(
            firstName="Jane",
            lastName="Doe",
            email="jane@example.com",
            phone="12345abcde",
            basicSalary=-100,
            deductions=200,
            joinDate="2026-05-01",
            user={"email": "jane@example.com", "role": "EMPLOYEE", "password": "secret"},
        )


def test_leave_application_dates_must_be_future():
    with pytest.raises(ValidationError):
        LeaveApplicationSchema(
            employeeId=1,
            type="VACATION",
            startDate="2020-01-01",
            endDate="2020-01-02",
            reason="Reason",
        )


def test_payslip_schema_month_range_validation():
    with pytest.raises(ValidationError):
        PayslipSchema(
            employeeId=1,
            month=13,
            year=2026,
            basicSalary=10000,
            allowances=100,
            deductions=50,
        )


def test_profile_schema_rejects_empty_bio():
    with pytest.raises(ValidationError):
        ProfileSchema(bio="")
