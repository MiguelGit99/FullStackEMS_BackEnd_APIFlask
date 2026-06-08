import logging
from apiflask import abort
from flask import jsonify, request
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from core.enums import UserRole

logger = logging.getLogger(__name__)

PUBLIC_ENDPOINTS = {
    "auth.login",
    "login",
    #"auth.refresh",
    "refresh",
    "core.health",
    "health",
    
    # Swagger, APIFlask y otros
    "openapi.spec",
    "openapi.docs",
    "static"
}

PUBLIC_BLUEPRINTS = {
    # "employee",
    # "attendance",
    # "profile"
}

# OPTIONAL_ENDPOINTS = {
#     #"profile.get_profile", 
# }

ROLES_BY_BLUEPRINT = {
    "employees": [UserRole.ADMIN],                      # Solo Admin ve empleados
    "attendance": [UserRole.ADMIN, UserRole.EMPLOYEE],  # Solo ADMIN y EMPLOYEE ven asistencias
    "leave_application": [UserRole.ADMIN, UserRole.EMPLOYEE],       # Solo Admin y EMPLOYEE gestionan permisos
    "profile": [UserRole.ADMIN, UserRole.EMPLOYEE],       
    "payslip": [UserRole.ADMIN, UserRole.EMPLOYEE],       
    "dashboard": [UserRole.ADMIN, UserRole.EMPLOYEE],      
    "products": [UserRole.ADMIN, UserRole.EMPLOYEE],      
}

ROLES_BY_ENPOINT = {
    "login": ["PUBLIC"],  # Cualquiera puede acceder sin tener un rol en especifico o sin estar logeado
    "refresh": [UserRole.ADMIN, UserRole.EMPLOYEE],  
    "logout": [UserRole.ADMIN, UserRole.EMPLOYEE],       
    "change_password": [UserRole.ADMIN, UserRole.EMPLOYEE]       
}




def register_auth_guard(app):

    @app.before_request
    def auth_guard():
        # Si es una petición de prueba de CORS, déjala pasar libremente
        if request.method == "OPTIONS":
            return
        
        if request.endpoint is None:
            return
        
         # B. Saltar validación de "JWT Required" si el Blueprint o el Endpoint es público
        if request.blueprint in PUBLIC_BLUEPRINTS or request.endpoint in PUBLIC_ENDPOINTS:
            return
        
        logger.info(f'Verifying JWT Request...')

        # Detectar si el endpoint actual es opcional (puede ser accedido tanto por usuarios autenticados como no autenticados)
        # is_optional = request.endpoint in OPTIONAL_ENDPOINTS
        
        # Validar JWT Required
        # 🔥 Stop API when JWT is not present or invalid
        try:
            verify_jwt_in_request() #optional=is_optional
        except Exception as e:
            logger.error(f"JWT Verification Failed: {str(e)}")
            # Forzamos un código 401 (No autorizado) que interrumpe la petición de inmediato
            abort(401, message="Missing or invalid Authorization Header Token")


        # Verificamos si el Blueprint que se intenta ejecutar tiene restricciones de rol
        #if request.blueprint in ROLES_BY_BLUEPRINT:
        claims = get_jwt()

        # if is_optional and not claims:
        #     # Dejamos pasar la petición libremente. Tu controlador (la función de la ruta) 
        #     # se encargará de retornar el JSON {"isValid": False, "user": None}, 200
        #     return 
        
        user_role = claims.get("role")
        
        endpoint_name = request.endpoint.rsplit(".", 1)[-1] if request.endpoint else None
        allowed_roles = []

        # Extraemos los roles permitidos según el nombre de endpoint o el blueprint
        allowed_roles = ROLES_BY_ENPOINT.get(request.endpoint, []) or ROLES_BY_ENPOINT.get(endpoint_name, [])
        if allowed_roles is None or len(allowed_roles) <= 0:
            allowed_roles = ROLES_BY_BLUEPRINT.get(request.blueprint, [])
        
        # if valid_roles is None or len(valid_roles) <= 0:
        #     allowed_roles = [role.value for role in valid_roles]
        
        # logger.info(f'role 1 = {role}')
        logger.info(f'Validaton Roles (allowed roles)= {allowed_roles}')
        # logger.info(f'allowed_roles 1 = {allowed_roles if allowed_roles else ""}')

        
        # allowed_roles = [role.value for role in valid_roles]
        # logger.info(f'allowed_roles 2 = {allowed_roles}')

        

        # Si el rol del empleado no está autorizado para este módulo, bloqueamos
        if user_role not in allowed_roles and "PUBLIC" not in allowed_roles:
            return jsonify({
                "message": f"Access denied: Your role '{user_role}' has no permission in module {request.blueprint}",
                "code": "insufficient_permissions"
            }), 403