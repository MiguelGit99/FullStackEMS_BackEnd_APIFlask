from apiflask import abort
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from blueprints.auth.models import User
from blueprints.employees.models import Employee
from blueprints.profile.schemas import ProfileSchema
from core.extensions import db


def update_profile(user_id: int, profile: ProfileSchema):

    stmt = (
        select(Employee)
        .options(joinedload(Employee.user))
        .where(Employee.userId == user_id)
    )
    
    db_employee = db.session.execute(stmt).scalar_one_or_none()

    if (db_employee is None):
        abort(404, "Employee not found")
    
    if (db_employee.isDeleted):
        abort(403, "Your account is deactivated. You cannot update your profile.")
    
    db_employee.bio = profile.bio

    db.session.commit()
    db.session.refresh(db_employee)

    return db_employee

