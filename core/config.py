from datetime import timedelta
import os

class Config:
    #FLASK_ENV = os.getenv('FLASK_ENV') 
    # Detectar el entorno (Por defecto asumimos producción por máxima seguridad)
    ENV = os.environ.get("FLASK_ENV", "production")
    IS_PRODUCTION = ENV == "production"

    # Sin esto, algunas excepciones internas/JWT/APIFlask no llegan correctamente al handler global (core/exceptionhandler.py).
    PROPAGATE_EXCEPTIONS = True

    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() in ['true', '1', 't']

    # Clave secreta para sesiones y seguridad
    #SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')

    # Configuración de CORS
    #CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

    #SECRET_KEY = os.environ.get("SECRET_KEY")
    
    # --- CONFIGURACIÓN FLASK-JWT-EXTENDED PARA REACT (2026) ---
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    #JWT_TOKEN_LOCATION = ["cookies"]          # Para PRD. Bloquea headers; fuerza el uso de cookies
    
    JWT_TOKEN_LOCATION = ["cookies"] if IS_PRODUCTION else ["headers", "cookies"]          
    #JWT_HEADER_NAME = "Authorization" # Nombre del header estándar (Por defecto es 'Authorization')
    #JWT_HEADER_TYPE = "Bearer"
    
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Seguridad de Cookies
    JWT_COOKIE_SECURE = IS_PRODUCTION                   
    JWT_COOKIE_HTTPONLY = True                # Impide que JavaScript (XSS) lea los tokens
    JWT_COOKIE_CSRF_PROTECT = IS_PRODUCTION   # Activa protección estricta contra CSRF 
    JWT_ACCESS_COOKIE_PATH = "/"
    JWT_REFRESH_COOKIE_PATH = "/api/auth/refresh" # El refresh token solo viaja a esta 
    
    # NUEVA LÍNEA CLAVE: Le dice a Flask-JWT-Extended que la verificación CSRF 
    # SOLO se exige cuando el token venga guardado dentro de una COOKIE.
    # Si el token viene de un Header (como el Authorize de Swagger), NO exigirá CSRF.
    JWT_CSRF_IN_COOKIES = True 
    # Evita que sitios web de terceros envíen tus cookies de sesión
    JWT_COOKIE_SAMESITE = "Strict" if IS_PRODUCTION else "Lax"

    SECURITY_SCHEMES = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        } 
    } if IS_PRODUCTION else {} # Solo cuando no es PRD

    SECURITY = [
        {
            "BearerAuth": []
        }
    ] if IS_PRODUCTION else [] # Solo cuando no es PRD