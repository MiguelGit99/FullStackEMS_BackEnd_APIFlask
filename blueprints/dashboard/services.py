from datetime import date

from apiflask import abort
from flask_jwt_extended import get_jwt
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
from blueprints.attendance.models import Attendance
from blueprints.dashboard.schemas import DashboardAdminResponseSchema, DashboardEmployeeResponseSchema
from blueprints.employees.models import Employee
from blueprints.leave_application.models import LeaveApplication
from blueprints.payslip.models import Payslip
from core.enums import Departments, LeaveStatus, UserRole
from core.extensions import db

def get_all_dashboard():
    claims = get_jwt()
    role = claims.get("role")
    employee_id = claims.get("employeeId")

    if role == UserRole.ADMIN:
        stmt_total_employees = select(func.count(Employee.id)).where(Employee.isDeleted != True)
        total_employees = db.session.scalar(stmt_total_employees)

        stmt_attendances_today = select(func.count(Attendance.id)).where(Attendance.date == date.today())
        attendances_today = db.session.scalar(stmt_attendances_today)

        stmt_leave_application_pending = (
            select(func.count(LeaveApplication.id))
            .where(LeaveApplication.status == LeaveStatus.PENDING)
        )
        leave_application_pending = db.session.scalar(stmt_leave_application_pending)

        dashboard = DashboardAdminResponseSchema (
            role = UserRole.ADMIN,
            totalEmployees = total_employees,
            totalDepartments = len(Departments),
            todayAttendance = attendances_today,
            pendingLeaves = leave_application_pending
        )

        return dashboard

    else:
        db_employee = db.session.get(Employee, employee_id)

        if db_employee is None:
            abort(404, "Employee not found")

        today = date.today()
        first_day_next_month = today
        if today.month == 12:
            first_day_next_month = date(today.year + 1, 1, 1)
        else:
            first_day_next_month = date(today.year, today.month + 1, 1)

        stmt_attendances_month = (
            select(func.count(Attendance.id))
            .where(
                Attendance.employeeId == employee_id,
                Attendance.date >= today.replace(day = 1),
                Attendance.date < first_day_next_month
            )
        )
        attendances_month = db.session.scalar(stmt_attendances_month)

        stmt_leave_application_pending = (
            select(func.count(LeaveApplication.id))
            .where(
                LeaveApplication.employeeId == employee_id,
                LeaveApplication.status == LeaveStatus.PENDING
            )
        )
        leave_application_pending = db.session.scalar(stmt_leave_application_pending)

        stmt_payslip_employee = (
            select(Payslip)
            .where(Payslip.employeeId == employee_id)
            .order_by(Payslip.createdAt.desc())
        )
        latet_payslip = db.session.scalars(stmt_payslip_employee).first()

        dashboard = DashboardEmployeeResponseSchema (
            role = UserRole.EMPLOYEE,
            employeeId = employee_id,
            employee = db_employee,
            currentMonthAttendance = attendances_month,
            pendingLeaves = leave_application_pending,
            latestPayslip = latet_payslip
        )

        return dashboard



