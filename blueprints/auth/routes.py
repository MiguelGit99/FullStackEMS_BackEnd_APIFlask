import logging
import json
from apiflask import APIBlueprint, abort
from flask import jsonify, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
from blueprints.auth.schemas import ChangePasswordSchema, LoginResponseSchema, LoginSchema
from blueprints.auth.services import update_password, verify_login
from core.decorators import log, roles_required
from flask import current_app

from core.enums import UserRole
from core.errorhandler import success_response

logger = logging.getLogger(__name__)

auth_bp = APIBlueprint('auth', 
                        __name__,
                        url_prefix='/api/auth')

@auth_bp.post('/login')
@auth_bp.input(LoginSchema, arg_name="data")
@auth_bp.output(LoginResponseSchema, status_code=200)
@auth_bp.doc(security=[])
#@log
def login(data: LoginSchema):
    user = verify_login(data)

    # logger.info("DEBUG:")
    # logger.info(current_app.debug)

    # JWT
    # 1. Generar los JWT criptográficos (Corren internamente tus handlers)
    # access_token = create_access_token(identity=user.id)
    # refresh_token = create_refresh_token(identity=user.id)
    # 2. Generar tokens criptográficos inyectando claims explícitos
    # identity recibe SOLO el string del ID. Los datos extra van en additional_claims
    claims = {
        "role": user.role, 
        "email": user.email, 
        "firstName": user.employee.firstName if user and user.employee else None, 
        "lastName": user.employee.lastName if user and user.employee else None,
        "employeeId": user.employee.id if user and user.employee else None,
        "employeePosition": user.employee.position if user and user.employee else None,
        "employeeBio": user.employee.bio if user and user.employee else None
    }

    access_token = create_access_token(
        identity=user.id,
        additional_claims=claims
    )
    refresh_token = create_refresh_token(
        identity=user.id,
        additional_claims=claims
    )

    data_response = {
        "isValid": True,
        "user": {
            "id": user.id,
            "role": user.role,
            "email": user.email,
            "firstName": claims.get("firstName"), 
            "lastName": claims.get("lastName"),
            "employeeId": claims.get("employeeId"),   
            "employeePosition": claims.get("employeePosition"),
            "employeeBio": claims.get("employeeBio")
        },
        "access_token": (access_token if "prod" not in current_app.config.get('FLASK_ENV', '') else "") # TODO: Solo para DEV  
    }
    
    # 2. CREAR UN OBJETO RESPONSE REAL (Soluciona el AttributeError)
    # Convertimos el diccionario a texto JSON y asignamos el Content-Type correcto
    response = make_response(
        # json.dumps(
        # success_response(data_response, message='Login successfull')
    #)
    data_response
    , 200)
    response.headers["Content-Type"] = "application/json"

    #response =  jsonify(success_response(data_response, message='Login successfull'))
        

    # 3. Inyectar cookies HttpOnly silenciosas
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response

@auth_bp.post("/refresh")
#@jwt_required(refresh=True) # Requiere estrictamente la cookie de refresco
@roles_required(UserRole.ADMIN, UserRole.EMPLOYEE)
#@auth_bp.doc(security=[])
def refresh():
    user_id = get_jwt_identity()
    claims = get_jwt()
    
    # Generar instancia de objeto user_payload (tipo LoginResponseSchema) con sus valores
    user_payload = {
        "isValid": True,
        "user": {
            "id": user_id,
            "role": claims.get("role"),
            "email": claims.get("email")
        }
    }
    
    new_access_token = create_access_token(identity=user_payload.user.id)
    
    response = user_payload
    #response = jsonify({"message": "Token actualizado correctamente"})
    #response = success_response(user_payload, message='Token successfully updated')
    
    set_access_cookies(response, new_access_token)
    return response

#@jwt_required(refresh=True) # Requiere estrictamente la cookie de refresco
@roles_required(UserRole.ADMIN, UserRole.EMPLOYEE)
@auth_bp.post("/logout")
def logout():
    response = jsonify({"message": "Session successfully closed."})
    unset_jwt_cookies(response) # Elimina por completo las cookies del navegador
    return response

#@log
@auth_bp.post("/change_password")
#@jwt_required()
@roles_required(UserRole.ADMIN, UserRole.EMPLOYEE)
@auth_bp.input(ChangePasswordSchema, arg_name="data")
# @auth_bp.doc(security="BearerAuth") # TODO: Esta ultima linea solo es para DEV
def change_password(data):
    current_user_id = get_jwt_identity()
   
    # # Claims cifradas dentro del JWT
    # claims = get_jwt()
    # user_role = claims.get("role")
    # user_email = claims.get("email")

    #logger.info(f'current_user_id={current_user_id}')
#if not current_user_identity or len(current_user_identity.strip()) == 0:
    if(current_user_id is None or 
       len(current_user_id.strip()) == 0 or 
       not str(current_user_id).strip().isdigit() or
       int(current_user_id) <= 0 ):
        abort(400, "Invalid session.")

    update_password(current_user_id, data)

    response = jsonify({"message": "Password successfully changed."})
    #return (response, 200)
     
    #response = success_response(data=None, message='Password successfully changed')

    return  response

# @auth_bp.post("/claims")
# def get_claims():
#     claims = get_jwt()
    
#     return jsonify({
#         "isValid": True, 
#         "user": {
#             "id": get_jwt_identity(), 
#             "role": claims.get("role"), 
#             "email": claims.get("email"),
#             "firstName": claims.get("firstName"), 
#             "lastName": claims.get("lastName"),
#             "employeeId": claims.get("employeeId")   
#         }
#     })

#     return claims