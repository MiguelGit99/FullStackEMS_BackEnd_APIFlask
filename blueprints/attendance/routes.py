import logging
from apiflask import APIBlueprint
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from pydantic import TypeAdapter
from blueprints.attendance.schemas import AttendanceLimitSchema, AttendancePlusInfoResponseSchema, AttendanceResponseSchema
from blueprints.attendance.services import get_all_attendance, register_clockIn
from core.errorhandler import success_response
#from flask import request
from flask_jwt_extended import get_jwt

logger = logging.getLogger(__name__)

attendance_bp = APIBlueprint("attendance", 
                         __name__,
                         url_prefix='/api/attendance') 
# # Cuando haya rutas publicas (que no requieran JWT) se agregan aquí así: { "attendance.healthcheck"}
# PUBLIC_ROUTES = set() 

# @attendance_bp.before_request
# def protect_routes():
#     """ 
#         Implementa de forma automática el @jwt_required en todas las funciones de este archivo routes.py 
#     """
#     if request.endpoint in PUBLIC_ROUTES:
#         return

#     verify_jwt_in_request()


# @attendance_bp.route("/<int:department_id>", methods=["GET"])
@attendance_bp.post("/")
#@employees_bp.get("/<string:department>")
#@jwt_required()
@attendance_bp.output(AttendanceResponseSchema, status_code=200)
#@attendance_bp.doc(security="BearerAuth") # TODO: Esta ultima linea solo es para DEV
def clockIn():
    #user_id = get_jwt_identity()
    claims = get_jwt()
    employee_id = int(claims["employeeId"]) if claims["employeeId"] else None
    
    db_attendance = register_clockIn(employee_id)

    #return success_response(db_attendance, operation='CHECK_OUT')
    return db_attendance


#@attendance_bp.get("/<int:limit>")
@attendance_bp.get("/")
# @attendance_bp.doc(security="BearerAuth") # TODO: Esta ultima linea solo es para DEV
#@jwt_required()
@attendance_bp.input(AttendanceLimitSchema, location='query', arg_name="data")
@attendance_bp.output(AttendancePlusInfoResponseSchema, status_code=200)
def get_attendance(data: AttendanceLimitSchema):
    claims = get_jwt()
    employee_id = int(claims["employeeId"]) if claims["employeeId"] else None

    # logger.info(f'EMPLOYEE_ID = {employee_id}')
    # logger.info(f'data = {data}')

    #{ history_attendance, employee_isDeleted } = get_all_attendance(employee_id, limit)
    attendance_list, isDeleted = get_all_attendance(employee_id, data.limit)

    if attendance_list is None:
        return []
    
    # return {
    #     'list': attendance_list,
    #     'isDeleted': isDeleted
    # }

    #return success_response(data)

    #return attendance_list

    # Filtramos la lista para asegurarnos de eliminar cualquier elemento None
    # Esto garantiza que todos los elementos enviados a APIFlask sean objetos válidos
    clean_attendance_list = [record for record in attendance_list if record is not None]

    # logger.info(f"attendance list...")
    # lista_serializable = TypeAdapter(list[AttendanceResponseSchema]).dump_python(clean_attendance_list, mode="json")
    # logger.info(f"lista_serializable = {lista_serializable}")
    

    response = {
        "attendanceList": clean_attendance_list,
        "employeeIsDeleted": isDeleted
    }

    return response
