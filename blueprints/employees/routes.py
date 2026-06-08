import logging
from apiflask import APIBlueprint, abort
from flask import jsonify, request
from blueprints.employees.services import ( get_all_employees, create_employee, get_employee, soft_delete_employee, update_employee )
from blueprints.employees.schemas import EmployeeCreateSchema, EmployeeResponseSchema, EmployeeSearchSchema, EmployeeUpdateSchema

logger = logging.getLogger(__name__)

employees_bp = APIBlueprint("employees", 
                         __name__,
                         url_prefix='/api/employees') 
#employees_bp.strict_slashes=False

# @employees_bp.route("/<int:department_id>", methods=["GET"])
@employees_bp.get("/")
# @employees_bp.get("/<string:department>")
# @jwt_required()
@employees_bp.input(EmployeeSearchSchema, location='query', arg_name="data")
@employees_bp.output(list[EmployeeResponseSchema], status_code=200)
# @employees_bp.doc(security="BearerAuth") # TODO: Esta ultima linea solo es para DEV
def list_employees(data: EmployeeSearchSchema): #department: str = None
    # """Obtiene la lista de empleados, opcionalmente filtrada por departamento
    # ---
    # tags:
    #   - Employees
    # parameters:
    #   - name: department_id
    #     in: path
    #     type: string
    #     required: false
    # responses:
    #   200:
    #     description: Lista de empleados obtenida exitosamente
    #     schema:
    #       type: array
    #       items:
    #         $ref: '#/definitions/EmployeeResponseSchema'
    #   400:
    #     description: Parámetro de departamento no válido
    #   500:
    #     description: Error interno del servidor    
    # """
    # employees = get_all_employees(department_id)

    # serialized_employees = [
    #     EmployeeSchema.model_validate(e).model_dump(mode='json') # mode-json ayuda a serializar correctamente Decimal, datetime, UUID y otros tipos especiales
    #     for e in employees
    # ]

    # TODO: Agregar validators.py (employee y user) para validar el input del query param department_id y evitar que se hagan consultas innecesarias a la base de datos con valores no válidos
    
    # return EmployeeSchema(many=True).model_validate(employees).model_dump(mode='json')

    #return EmployeeSchema(many=True).jsonify(employees)
    #return jsonify(serialized_employees), 200

    #return get_all_employees(department)

    #department = request.args.get('department', default=None, type=str)
    employee_list = get_all_employees(data.department)

    #logger.info(f'COUNT EMPLOYEES: {len(employee_list)}')

    # serialized = [
    #     EmployeeResponseSchema
    #     .model_validate(employee)
    #     .model_dump(mode="json")

    #     for employee in employee_list
    # ]

    return employee_list

# @employees_bp.route("/<int:employee_id>", methods=["GET"])
@employees_bp.get("/<int:employee_id>")
@employees_bp.output(EmployeeResponseSchema, status_code=200)
def get_employee_by_id(employee_id):
    # employee = Employee.query.get_or_404(employee_id)
    # return EmployeeSchema().model_validate(employee).model_dump(mode='json')

    # return db.session.execute(
    #     select(Employee).where(Employee.id == employee_id)
    # ).scalars().all()

    return get_employee(employee_id)

    # employee = get_employee(employee_id)

    # return success_response(employee)


# @employees_bp.route("/", methods=["POST"])
@employees_bp.post("")
#@roles_required(UserRole.ADMIN)
@employees_bp.input(EmployeeCreateSchema, arg_name="data")
@employees_bp.output(EmployeeResponseSchema, status_code=201)
# @employees_bp.doc(security="BearerAuth") # TODO: Esta ultima linea solo es para DEV
def add_employee(data):
    # employee = request.get_json()

    # validated_employee = EmployeeSchema().model_validate(employee) # Validamos el input usando el Schema

    #logger.info(f"data: {data}")

    new_employee = create_employee(data)

    #logger.info(f"new_employee: {new_employee}")

    # response = EmployeeResponseSchema.model_validate(new_employee).model_dump(mode="json")
    # return jsonify({"message": "Empleado creado exitosamente", "employee": response}), 201

    return new_employee

    #return success_response(new_employee, message='Employee successfully added')


# @employees_bp.route("/<int:employee_id>", methods=["PUT"])
@employees_bp.patch("")
@employees_bp.input(EmployeeUpdateSchema, arg_name="data")
@employees_bp.output(EmployeeResponseSchema, status_code=200)
def edit_employee(data: EmployeeUpdateSchema):
    # validated_employee = EmployeeSchema().model_validate(employee) # Validamos el input usando el Schema
    
    updated_employee = update_employee(data)

    # if updated_employee is None:
    #     abort(404, message="Employee not found")
    

    # if not updated_employee:
    #     return jsonify({"message": "Empleado no encontrado"}), 404

    # response = EmployeeResponseSchema.model_validate(updated_employee).model_dump(mode="json")
    # return jsonify({"message": "Empleado actualizado exitosamente", "employee": response}), 200

    return updated_employee
    #return success_response(updated_employee, message='Employee successfully updated')

@employees_bp.delete("/<int:employee_id>")
@employees_bp.doc(summary="Soft delete employee")
def delete_employee(employee_id): 
    soft_delete_employee(employee_id)
    return {}, 204

    #return success_response(employee_id, message='Employee marked as deleted successfully')
    