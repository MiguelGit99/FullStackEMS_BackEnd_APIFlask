import os
from types import SimpleNamespace
import pytest
from flask_jwt_extended import create_access_token

# Force testing configuration before importing the app
os.environ["FLASK_ENV"] = "testing"
os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

from app import create_app
from core.extensions import db

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        # Import models so SQLAlchemy metadata is registered
        from blueprints.auth.models import User
        from blueprints.employees.models import Employee
        from blueprints.attendance.models import Attendance
        from blueprints.leave_application.models import LeaveApplication
        from blueprints.payslip.models import Payslip
        from blueprints.products.models import Product, Brand

        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_headers(app):
    with app.app_context():
        token = create_access_token(
            identity="1",
            additional_claims={
                "role": "ADMIN",
                "email": "admin@example.com",
                "firstName": "Admin",
                "lastName": "User",
                "employeeId": 1,
            },
        )
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def employee_headers(app):
    with app.app_context():
        token = create_access_token(
            identity="2",
            additional_claims={
                "role": "EMPLOYEE",
                "email": "employee@example.com",
                "firstName": "Employee",
                "lastName": "User",
                "employeeId": 2,
            },
        )
    return {"Authorization": f"Bearer {token}"}
