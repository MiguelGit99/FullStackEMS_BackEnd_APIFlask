from flask import jsonify #, make_response
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException
import logging
from apiflask import HTTPError
from werkzeug.exceptions import BadRequest
from core.extensions import db
from sqlalchemy.exc import IntegrityError
from apiflask import HTTPError

logger = logging.getLogger(__name__)

# def _build_response(payload, status_code=200, headers=None):
#     response = make_response(jsonify(payload), status_code)
#     response.headers["Content-Type"] = "application/json; charset=utf-8"
#     if headers:
#         for key, value in headers.items():
#             response.headers[key] = value
#     return response


# def success_response(data=None, status_code=200, meta=None, headers=None):
#     payload = {
#         "status": "success",
#         "data": data
#     }
#     if meta is not None:
#         payload["meta"] = meta
#     return _build_response(payload, status_code, headers)

def success_response(data, status_code=200, message=None, operation=None):
    return {
        'status': 'success', 
        'status_code':status_code, 
        'operation':operation, 
        'message':message, 
        'data': data
    }

# def error_response(message, status_code=400, code=None, details=None, headers=None):
#     """
#     Generate a standardized error response payload for API endpoints.

#     Args:
#         message (str): The error message to include in the response.
#         status_code (int, optional): HTTP status code for the response. Defaults to 400.
#         code (int or str, optional): Custom error code to include in the response. If not provided, uses status_code.
#         details (Any, optional): Additional details about the error to include in the response.
#         headers (dict, optional): Additional headers to include in the response.

#     Returns:
#         Response: A Flask response object containing the error payload and status code.
#     """
#     payload = {
#         "status": "error",
#         "message": message,
#         "code": code or status_code
#     }
#     if details is not None:
#         payload["details"] = details
#     return _build_response(payload, status_code, headers)

def error_response(message, status_code=400, details=None):
    return jsonify({
        'status': 'error', 
        'message': message, 
        'code': status_code, 
        'details':details
    }), status_code

def register_error_handlers(app):
    
    # @app.errorhandler(401)
    # def bad_request(e):
    #     return e

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        logger.exception(e)

        return error_response(
            message=e.description,
            status_code=e.code,
            #code=e.code
        )

    @app.errorhandler(Exception)
    def handle_unexpected_exception(e):
        logger.exception(e)

        # En producción no conviene exponer str(e) al cliente.
        return error_response(
            message="Error interno del servidor", #str(e),
            status_code=500,
            #code=500
        )
    
    @app.errorhandler(HTTPError)
    def handle_apiflask_error(e):

        logger.exception(e)

        return error_response(
            message=e.message,
            status_code=e.status_code
        )
    
    @app.errorhandler(BadRequest)
    def handle_bad_request(e):

        logger.exception(e)

        return error_response(
            message="Invalid request body",
            status_code=400
        )
    
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e):

        db.session.rollback()

        logger.exception(e)

        return error_response(
            message="Database integrity error",
            status_code=409
        )
    

    @app.error_processor
    def handle_apiflask_errors(error):

        status_code = getattr(error, "status_code", 500)

        message = getattr(error, "message", "Internal server error")

        detail = getattr(error, "detail", {})

        if status_code >= 500:
            logger.exception(error)
        else:
            logger.warning(error)

        # return {
        #     "status": "error",
        #     "message": message,
        #     "details": detail,
        #     "code": status_code
        # }, status_code

        return error_response(
            message=message,
            status_code=status_code,
            details=detail
        )
            
    # @app.errorhandler(Exception)
    # def handle_unexpected_exception(e):
    #     # En producción no conviene exponer str(e) al cliente.
    #     return error_response(
    #         message="Error interno del servidor", #str(e),
    #         status_code=500,
    #         code=500
    #     )

    # @app.errorhandler(400)
    # def bad_request(e):
    #     return jsonify({'status': 'error', 'message': 'Petición incorrecta', 'code': 400}), 400
    
    # @app.errorhandler(404)
    # def not_found(e):
    #     return jsonify({'status': 'error', 'message': 'Recurso no encontrado', 'code': 404}), 404

    # @app.errorhandler(500)
    # def internal_error(e):
    #     return jsonify({'status': 'error', 'message': 'Error interno del servidor', 'code': 500}), 500
    

    # @app.errorhandler(HTTPException)
    # def handle_exception(e):
    #     # e.code es el código de error (ej. 404, 500)
    #     # e.description es la descripción detallada
    #     #return render_template("error.html", error=e), e.code
    #     return jsonify({'status': 'error', 'message': 'Error interno del servidor', 'code': e.status}), e.status
    
    # # Opcional: Si quieres un manejo aún más genérico, 
    # # incluso para excepciones que no son de HTTP (como errores 500 internos)
    # @app.errorhandler(Exception)
    # def handle_generic_exception(e):
    #     # Esto captura cualquier otra excepción no manejada
    #     return {"error": "Error interno del servidor", "message": str(e)}, 500


def register_db_handlers(app):
    @app.teardown_request
    def teardown_request(exception=None):

        if exception:
            db.session.rollback()