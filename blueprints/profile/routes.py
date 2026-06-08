import logging
from apiflask import APIBlueprint
from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from blueprints.profile.schemas import ProfileSchema
from blueprints.profile.services import update_profile

logger = logging.getLogger(__name__)

profile_bp = APIBlueprint("profile",
                          __name__,
                          url_prefix="/api/profile")

@profile_bp.get("")
@profile_bp.get("/")
#@jwt_required()
# @profile_bp.doc(security="BearerAuth") # TODO: Esta ultima linea solo es para DEV
def get_profile():
    # logger.info("claims")
    # logger.info(claims)

    claims = get_jwt()
    #claims["email"]

    # Genera objeto nuevo sin haber definido su clase previamente
    response = {
        # "email": claims["email"],
        # "role":  claims["role"],
        # "firstName": claims["firstName"] if claims["firstName"] else "Administrator",
        # "lastName": claims["lastName"],

        "isValid": claims is not None and claims.get("email") is not None,  # Si no hay claims o no hay email, entonces el token no es válido
        "user": {
            "id": get_jwt_identity(), 
            "role": claims.get("role"), 
            "email": claims.get("email"),
            #"firstName": claims.get("firstName") if claims.get("firstName") else "Administrator", 
            "firstName": claims.get("firstName"), 
            "lastName": claims.get("lastName"),
            "employeeId": claims.get("employeeId")   
        }
    }

    return jsonify(response)

@profile_bp.post("/")
#@jwt_required()
@profile_bp.input(ProfileSchema, arg_name="data")
# @profile_bp.doc(security="BearerAuth") # TODO: Esta ultima linea solo es para DEV
def edit_profile(data: ProfileSchema):
    user_id = get_jwt_identity()
    
    update_profile(user_id, data)

    response = jsonify({"message": "Profile successfully changed."})

    return response, 200


    



