import logging
from apiflask import abort
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import load_only, joinedload
from blueprints.employees.models import Employee
from blueprints.employees.schemas import EmployeeCreateSchema, EmployeeUpdateSchema
from core.extensions import db
from blueprints.auth.models import User
from core.enums import Departments, EmploymentStatus, UserRole
from core.decorators import log

logger = logging.getLogger(__name__)

def get_employee(employee_id: str):
    stmt = (
        select(Employee)
        .options(
            joinedload(Employee.user)
        )
        .where(
            Employee.id == employee_id
        )
    )

    employee = (
        db.session.execute(stmt)
        .scalar_one_or_none()
    )

    # logger.info(f"Employe response...")
    # res_serializable = TypeAdapter(EmployeeResponseSchema).dump_python(employee, mode="json")
    # logger.info(f"res_serializable = {res_serializable}")
    

    if employee is None:
        abort(404, "Employee not found")
        
    return employee

def get_all_employees(department: str | None = None):
    """
    Obtiene la lista de empleados desde la base de datos
    ---
    tags:
      - Employees
    responses:
      200:
        description: Lista de empleados obtenida exitosamente
        schema:
          type: array
          items:
            $ref: '#/definitions/Employee'
    """

    #logger.info("GET ALL EMPLOYEES SERVICE - DEPARTMENT FILTER: %s", department)

    # Usa joinedload para cargar la relación con User de todos los empleados de una sola vez.
    # Ya que Employees.query.all() realiza un query aparte por cada empleado para cargar su usuario asociado, 
    # lo que puede generar un problema de N+1 queries.

    stmt = (
        select(Employee)
        .options(
            # load_only(
            #     Employee.id,
            #     Employee.firstName,
            #     Employee.lastName
            # ),

            joinedload(Employee.user).load_only(
                User.id,
                User.email,
                User.role
            )
        )
        #.options(joinedload(Employee.user))
        #.where(Employee.department == department_id)
        # .order_by(Employee.first_name)
    )

    if department is not None:
        #employees = db.session.options(db.joinedload(Employee.user)).where(Employee.department == department_id).all()
        stmt = stmt.where(Employee.department == department)
       
    employees = (
        db.session.execute(stmt)
        .scalars()
        .all()
    )

    # logger.info(f"Employee list...")
    # lista_serializable = TypeAdapter(list[EmployeeResponseSchema]).dump_python(employees, mode="json")
    # logger.info(f"lista_serializable = {lista_serializable}")
    

    return employees

# Funcion para crear un empleado nuevo, que también crea un usuario 
# @log
def create_employee(employee: EmployeeCreateSchema):
    """
    Crea un nuevo empleado junto con su usuario asociado
    ---
    tags:
      - Employees
    parameters:
        - name: employee
            in: body
            required: true
            schema:
            $ref: '#/definitions/EmployeeInput'
    responses:
      201:
        description: Empleado creado exitosamente
        schema:
          $ref: '#/definitions/Employee'
    """
    # Primero creamos el usuario
    new_user = User(
        email=employee.email,
        role=employee.user.role if employee.user.role else UserRole.EMPLOYEE
    )
    new_user.hash_password(employee.user.password)

    #logger.info(f"User Password: {new_user.password} , Employee Pass: {employee.user.password}")

    try:
        db.session.add(new_user)
        #db.session.commit()  # Necesitamos hacer commit para obtener el userId generado
        db.session.flush()  # flush() envía los cambios a la base de datos sin hacer commit, lo que nos permite obtener el userId generado
    except IntegrityError as e:
        db.session.rollback()

        if "UNIQUE KEY" in str(e.orig):
            abort(
                400,
                description=(
                    "User Email already exists"
                )
            )
        raise

    employee.userId = new_user.id  # Asignamos el userId al empleado para crear la relación entre ambos

    # Luego creamos el empleado asociado al usuario recién creado
    new_employee = Employee(
        userId=new_user.id,
        firstName=employee.firstName,
        lastName=employee.lastName,
        email=employee.email,
        phone=employee.phone,
        position=employee.position,
        basicSalary=employee.basicSalary,
        allowances=employee.allowances,
        deductions=employee.deductions,
        employmentStatus=employee.employmentStatus,
        joinDate=employee.joinDate,
        bio=employee.bio or "",
        department=employee.department or Departments.ENGINEERING
    )

    try:
        db.session.add(new_employee)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()

        if "UNIQUE KEY" in str(e.orig):
            abort(
                400,
                description=(
                    "Employee Email already exists"
                )
            )
        raise

    return new_employee

def update_employee(employee: EmployeeUpdateSchema):
    """
    Actualiza la información de un empleado existente
    ---
    tags:
      - Employees
    parameters:
        - name: employee
            in: body
            required: true
            schema:
            $ref: '#/definitions/EmployeeUpdate'
    responses:
      200:
        description: Empleado actualizado exitosamente
        schema:
          $ref: '#/definitions/Employee'
        404:
        description: Empleado no encontrado
    """
    # employee = Employee.query.get(employee.id)
    # if not employee:
    #     return None  # O lanzar una excepción personalizada

    # # Actualizamos los campos del empleado
    # employee.firstName = employee.firstName
    # employee.lastName = employee.lastName
    # employee.department = employee.department
    # # Aquí podrías actualizar otros campos según sea necesario

    # db.session.commit()
    # return employee

    # stmt = (
    #     select(Employee)
    #     .where(
    #         Employee.id == employee.id
    #     )
    # )

    # db_employee = (
    #     db.session.execute(stmt)
    #     .scalar_one_or_none()
    # )
    
    db_employee = db.session.get(Employee, employee.id)

    if db_employee is None:
        abort(404, message="Employee not found")
        #return None
    
    update_data = employee.model_dump(
        exclude_unset=True
    )

    # 🔥 Eliminamos las llaves que corresponden a relaciones o llaves primarias
    # para evitar que 'setattr' intente meter datos inválidos en el modelo de SQLAlchemy
    update_data.pop("id", None)
    update_data.pop("userId", None)
    user_data = update_data.pop("user", None)
    # Eliminamos las llaves que no queremos modificar del usuario (id, contraseña)
    user_data.pop("id", None)
    if user_data.get("password") is None or len(user_data.get("password").strip()) == 0:
        user_data.pop("password", None)
    
    # Get and update user when defined in request (PATCH)
    if user_data and db_employee.userId:
        # Get user
        db_user = db.session.get(User, db_employee.userId)
        if db_user:
            # Update user field values (email, username, etc.)
            for key, value in user_data.items():
                # if key not in ["id", "password"]:
                if key != "password": 
                    setattr(db_user, key, value)
                else:
                    db_user.hash_password(value)  # Si se envía un nuevo password, lo hasheamos antes de guardarlo


    
    # Update employee field values
    for key, value in update_data.items():
        setattr(db_employee, key, value)

    db.session.commit()
    db.session.refresh(db_employee)

    return db_employee

def soft_delete_employee(employee_id):
    # stmt = select(Employee).where(Employee.id == employee_id)
    # employee = (db.session.execute(stmt).scalar_one_or_none())
    # db.session.delete(employee)
    # db.session.commit()

    if employee_id is None or len(str(employee_id).strip()) <= 0:
        abort(400, description="Invalid Employee")

    # Soft Delete
    stmt = (
        select(Employee)
        .where(
            Employee.id == employee_id,
            Employee.isDeleted == False
        )
    )

    employee = (db.session.execute(stmt).scalar_one_or_none())

    #logger.info(f"Employee data: {employee}")

    # if employee is None:
    #     abort(
    #         404,
    #         description=(
    #             "Employee not found"
    #         )
    #     )

    if employee is None:
        abort(404, description="Employee not found or already deleted")

    employee.isDeleted = True
    employee.employmentStatus = EmploymentStatus.INACTIVE
    db.session.commit()
