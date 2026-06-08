# app/core/jwt_handlers.py
import logging
from flask import jsonify
from .extensions import jwt

logger = logging.getLogger(__name__)


# @jwt.additional_claims_loader
# def add_claims_to_access_token(user_data):
#     return {
#         "role": user_data.role,
#         "email": user_data.email
#     }

@jwt.user_identity_loader
def user_identity_lookup(user_data):
    # if isinstance(user_data, dict):
    #     return str(user_data.id)
    return str(user_data)

# --- CAPTURA DE ERRORES HOMOGÉNEA ---
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    logger.warning(f'Token expired: {jwt_payload}')
    return jsonify({"message": "Token expired.", "code": "token_expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    logger.warning(f'Invalid token: {error}')
    return jsonify({"message": "Invalid token.", "code": "token_invalid"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    logger.warning(f'Missing token: {error}')
    return jsonify({"message": "Missing credentials", "code": "token_missing"}), 401
