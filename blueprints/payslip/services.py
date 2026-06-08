from decimal import Decimal
import logging

from apiflask import abort
from flask_jwt_extended import get_jwt
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from blueprints.employees.models import Employee
from blueprints.payslip.models import Payslip
from core.enums import UserRole
from core.extensions import db
from blueprints.payslip.schemas import PayslipResponseSchema, PayslipSchema

logger = logging.getLogger(__name__)

def create_payslip(payslip: PayslipSchema):
    db_employee = db.session.get(Employee, payslip.employeeId)
    
    stmt = (
        select(Payslip)
        .options(joinedload(Payslip.employee))
        .where(Payslip.employeeId == payslip.employeeId)
    )

    db_payslip = db.session.execute(stmt).scalar()

    if db_employee is None:
        abort(404, "Employee not found") 

    if db_employee.isDeleted:
        abort(404, "Your account is deactivated. You cannot add payslip.") 

    db_payslip = Payslip (
        employeeId = payslip.employeeId,
        month = payslip.month,
        year = payslip.year,
        basicSalary = payslip.basicSalary,
        allowances = payslip.allowances,
        deductions = payslip.deductions,
        netSalary = payslip.basicSalary + (payslip.allowances or Decimal(0)) - (payslip.deductions or Decimal(0)) 
    )

    db.session.add(db_payslip)
    db.session.commit()
    db.session.refresh(db_payslip)

    return db_payslip

def get_all_payslip():
    claims = get_jwt()
    role = claims.get("role")
    employee_id = claims.get("employeeId")

    logger.info(f"role: {role}")
    logger.info(f"employee_id: {employee_id}")

    if role == UserRole.ADMIN:
        stmt = (
            select(Payslip)
            .options(
                joinedload(Payslip.employee)
                .load_only(
                    Employee.id,
                    Employee.firstName,
                    Employee.lastName,
                    Employee.isDeleted
                )    
            )
            .order_by(Payslip.createdAt.desc())
        )

    else:
        db_employee = db.session.get(Employee, employee_id)

        if db_employee is None:
            abort(404, "Employee not found")

        stmt = (
            select(Payslip)
            .options(
                joinedload(Payslip.employee)
            )
            .where(Payslip.employeeId == employee_id)
            .order_by(Payslip.createdAt.desc())
        )

    db_payslips = db.session.execute(stmt).scalars().all()


    # if Payslip.employee is None:
    #     abort(404, "Employee not found") 

    # if Payslip.employee.isDeleted:
    #     abort(404, "Your account is deactivated. You cannot add payslip.") 

    return db_payslips

    

def get_payslip(id: int):
    stmt = (
        select(Payslip)
        .options(joinedload(Payslip.employee))
        .where(Payslip.id == id)
        .order_by(Payslip.createdAt.desc())
    )

    db_payslip = db.session.execute(stmt).scalar()
    
    # if Payslip.employee is None:
    #     abort(404, "Employee not found") 

    # if Payslip.employee.isDeleted:
    #     abort(404, "Your account is deactivated. You cannot add payslip.") 

    return db_payslip
