import json
import logging

from apiflask import abort
from flask import jsonify
from flask_jwt_extended import get_jwt
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from blueprints.employees.models import Employee
from blueprints.leave_application.models import LeaveApplication
from blueprints.leave_application.schemas import LeaveApplicationSchema, LeaveApplicationUpdateStatusSchema
from core.enums import LeaveStatus, UserRole
from core.extensions import db

logger = logging.getLogger(__name__)

def add_leave(leave: LeaveApplicationSchema):
    db_employee = db.session.get(Employee, leave.employeeId)

    if db_employee is None:
        abort(404, description="Employee not found")
    
    if db_employee.isDeleted:
        abort(403, description="Your account is deactivated. You cannot apply for leave.")
    

    new_leave = LeaveApplication(
        employeeId = leave.employeeId,
        type = leave.type,
        startDate = leave.startDate,
        endDate = leave.endDate,
        reason = leave.reason,
        status = LeaveStatus.PENDING
    )

    try:
        db.session.add(new_leave)
        db.session.commit()
        db.session.refresh(new_leave)
    except IntegrityError as e:
        db.session.rollback()

        if "UNIQUE KEY" in str(e.orig):
            abort(
                400,
                description=(
                    "Leave employeeId already exists"
                )
            )
        raise

    return new_leave
    

def get_all_leaves(data):
    claims = get_jwt()
    employee_id = int(claims.get("employeeId")) if claims.get("employeeId") else None
    role = claims.get("role")
    
    if role == UserRole.ADMIN:
        stmt = (
            select(LeaveApplication)
            .options(
                joinedload(LeaveApplication.employee).load_only(
                    Employee.firstName,
                    Employee.lastName,
                    Employee.isDeleted
                )    
            )
            #.execution_options(populate_existing=True) # Indica que no tome los datos de cache, solo lo mas reciente de SQL Server
        )
        
        if data.status:
            stmt = stmt.where(LeaveApplication.status == data.status)

        stmt = stmt.order_by(LeaveApplication.createdAt.desc())
        leaves = db.session.execute(stmt).scalars().all()

        lista_serializable = TypeAdapter(list[LeaveApplicationSchema]).dump_python(leaves, mode="json")
        #logger.info(f"Lista de esquemas recibida: {json.dumps(lista_serializable, indent=2)}")

        return lista_serializable
    else:
        db_employee = db.session.get(Employee, employee_id)

        if db_employee is None:
            abort(404, "Employee not found")

        #db_leave = db.session.get(LeaveApplication, employee_id)

        stmt = (
            select(LeaveApplication)
            .options(
                #joinedload(LeaveApplication.employee)
                joinedload(LeaveApplication.employee).load_only(
                    Employee.isDeleted
                ) 
            )
            #.execution_options(populate_existing=True) # Indica que no tome los datos de cache, solo lo mas reciente de SQL Server
            .where(LeaveApplication.employeeId == employee_id)
            .order_by(LeaveApplication.createdAt.desc())
        )

        # # Mapeo de la lista transformando cada elemento (.map() de la imagen)
        # # by_alias=True asegura que las llaves del JSON salgan en camelCase (createdAt, employeeId)
        # data = [LeaveApplicationResponse.transform(leave).model_dump(by_alias=True) for leave in leaves]


        db_leaves = db.session.execute(stmt).scalars().all()
        lista_serializable = TypeAdapter(list[LeaveApplicationSchema]).dump_python(db_leaves, mode="json")
        
        return lista_serializable


def update_leave_status(leave: LeaveApplicationUpdateStatusSchema):
    logger.info("leave.employeeId...")
    if leave is None:
        logger.info("leave is NONE")
    else:
        logger.info("leave is NOT NONE")

    lista_serializable = TypeAdapter(LeaveApplicationUpdateStatusSchema).dump_python(leave, mode="json")
    logger.info("leave lista_serializable")
    logger.info(f"lista_serializable: {lista_serializable}")

    
    logger.info(f"leave.status: {leave.status}")
    logger.info(f"leave.employeeId: {leave.id}")
    # db_leave = db.session.get(LeaveApplication, leave.employeeId)
    stmt = (
        select(LeaveApplication)
        .where(
            #LeaveApplication.employeeId == leave.employeeId
            LeaveApplication.id == leave.id
        )
    )

    db_leave = db.session.execute(stmt).scalar()

    if db_leave is None:
        abort(404, "Leave Application employee not found")
    
    db_leave.status = leave.status
    db.session.commit()
    db.session.refresh(db_leave)

    return db_leave 
