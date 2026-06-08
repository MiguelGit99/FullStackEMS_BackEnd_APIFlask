
import logging

from apiflask import APIBlueprint

from blueprints.leave_application.schemas import LeaveApplicationSchema, LeaveApplicationSearchSchema, LeaveApplicationUpdateStatusSchema
from blueprints.leave_application.services import add_leave, get_all_leaves, update_leave_status
from core.enums import UserRole

logger = logging.getLogger(__name__)

leave_application_bp = APIBlueprint("leave_application",
                         __name__,
                         url_prefix="/api/leave_application")

@leave_application_bp.post("/")
@leave_application_bp.input(LeaveApplicationSchema, arg_name="data")
@leave_application_bp.output(LeaveApplicationSchema, status_code=201)
def create_leave(data: LeaveApplicationSchema):
    return add_leave(data)

@leave_application_bp.get("/")
@leave_application_bp.input(LeaveApplicationSearchSchema, location='query', arg_name="data")
@leave_application_bp.output(list[LeaveApplicationSchema], status_code=200)
def getLeaves(data: LeaveApplicationSearchSchema):
    return get_all_leaves(data)

#@roles_required(UserRole.ADMIN, UserRole.EMPLOYEE) # Solo Admin o Recursos Humanos pueden cambiar el estado
@leave_application_bp.patch("/")
@leave_application_bp.input(LeaveApplicationUpdateStatusSchema, arg_name="data")
@leave_application_bp.output(LeaveApplicationSchema, status_code=200)
def edit_leave_status(data: LeaveApplicationUpdateStatusSchema):
    return update_leave_status(data)