import logging
from apiflask import APIBlueprint, abort
from blueprints.payslip.schemas import PayslipResponseSchema, PayslipSchema
from blueprints.payslip.services import create_payslip, get_all_payslip, get_payslip
from core.decorators import log

logger = logging.getLogger(__name__)

payslip_bp = APIBlueprint("payslip", 
                         __name__,
                         url_prefix='/api/payslip') 

@payslip_bp.post("/")
@payslip_bp.input(PayslipSchema, arg_name="data")
@payslip_bp.output(PayslipResponseSchema, status_code=200)
def add_payslip(data: PayslipSchema):
    # #user_id = get_jwt_identity()
    # claims = get_jwt()
    # employee_id = int(claims["employeeId"]) if claims["employeeId"] else None
    
    db_payslip = create_payslip(data)

    #return success_response(db_attendance, operation='CHECK_OUT')
    return db_payslip

@payslip_bp.get("/")
@payslip_bp.output(list[PayslipResponseSchema], status_code=200)
def get_payslips():
    # claims = get_jwt()
    # employee_id = int(claims["employeeId"]) if claims["employeeId"] else None

    #{ history_attendance, employee_isDeleted } = get_all_attendance(employee_id, limit)
    payslip_list = get_all_payslip()

    if payslip_list is None:
        return []
    
    # Filtramos la lista para asegurarnos de eliminar cualquier elemento None
    # Esto garantiza que todos los elementos enviados a APIFlask sean objetos válidos
    # clean_payslip_list = [record for record in payslip_list if record is not None]

    return payslip_list

@payslip_bp.get("/<int:id>")
#@payslip_bp.input(PayslipSearchSchema, arg_name="data")
@payslip_bp.output(PayslipResponseSchema, status_code=200)
@log
def get_payslip_by_id(id: int):
    payslip = get_payslip(id) 

    logger.info("EJECUTANDO get_payslip")
    logger.info(f"id={id}")
    logger.info(f"payslip is None={payslip is None}")

    # Si el servicio no encuentra el recibo, abortamos con un 404 controlado
    if payslip is None:
        abort(404, message="Payslip not found")
    
    return payslip