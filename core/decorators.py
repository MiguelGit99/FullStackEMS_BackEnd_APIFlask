import time
import logging
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

from core.enums import UserRole

# Decorador para medir el tiempo de ejecución de una función
# Uso: @timer()
def timer(language='en'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            if language == 'es':
                message = f"La función tardó: {end_time - start_time:.3f} segundos"
            else:
                message = f"Function execution time: {end_time - start_time:.3f} seconds"
            print(message)
            logging.info(message)
            return result
        return wrapper
    return decorator

# Uso directo sin parámetros: @timerlog
def timerlog(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        message = f"La función tardó: {end_time - start_time:.3f} segundos"
        print(message)
        logging.info(message)
        return result
    return wrapper

def log(func):
    #def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f'Initiating function %s.%s [target=%s | linea:%s]. [args: %s | kwargs: %s]', 
                        func.__module__,
                        func.__qualname__,             # Nombre completo de función (tambien se puede usar "func.__name__")
                        func.__code__.co_filename,     # Nombre de archivo original (el archivo que usa el decorador)
                        func.__code__.co_firstlineno,  # Línea de la ruta
                        args,
                        kwargs)  
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            import json
            logging.exception(f'EXCEPTION in function %s.%s. | args: %s | kwargs: %s',
                            func.__module__,
                            func.__qualname__,
                            # type(e).__name__,
                            # repr(e),
                            # vars(e),
                            # getattr(e, "args", None),     # Argumentos del objeto e (Exception)
                            # getattr(e, "__dict__", {},    # Si la excepcion tiene definido __dict__
                            args,
                            kwargs
            )
            raise
        logging.info(f'End of function %s.%s',
                        func.__module__,
                        func.__qualname__)
        return result
    return wrapper
    #return decorator    


def roles_required(*roles: UserRole):
    """
    Decorador para restringir el acceso a ciertos roles por medio de JWT.
    Acepta múltiples roles, por ejemplo: @roles_required(UserRole.ADMIN, UserRole.HR)
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # 1. Asegura que el JWT sea válido primero (actúa como @jwt_required)
            verify_jwt_in_request()
            
            # 2. Obtiene los claims del token descifrado
            claims = get_jwt()
            user_role = claims.get("role")
            
            # 3. Valida si el rol del usuario está en la lista de roles permitidos
            if user_role not in [role.value for role in roles]:
                return jsonify({
                    "message": "Access denied: Missing required permissions or user role has no access.",
                    "code": "insufficient_permissions"
                }), 403
                
            return fn(*args, **kwargs)
        return wrapper
    return decorator