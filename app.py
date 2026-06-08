import os
import profile

from flask_cors import CORS
from core.auth_guard import register_auth_guard
import core.jwt_handlers 
from flask import Flask, app
from dotenv import load_dotenv
from core.config import Config
from core.errorhandler import register_db_handlers, register_error_handlers
from core.request_context import register_request_context, register_cache_cleaner
from core.extensions import db, migrate, jwt
from core.logging_config import setup_logging
from apiflask import APIFlask
from core.routes import core_bp
from blueprints.products.routes import products_bp
from blueprints.employees.routes import employees_bp
from blueprints.auth.routes import auth_bp
from blueprints.profile.routes import profile_bp
from blueprints.attendance.routes import attendance_bp
from blueprints.leave_application.routes import leave_application_bp
from blueprints.payslip.routes import payslip_bp
from blueprints.dashboard.routes import dashboard_bp

# Load environment variables from .env file
load_dotenv(override=True)

def create_app():
    setup_logging()  # Configurar el logging antes de crear la aplicación

    #app = Flask(__name__)
    app = APIFlask(__name__)

    app.config.from_object(Config)

    # Ajustamos las opciones del motor según la base de datos utilizada.
    database_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "") or ""
    if database_uri.startswith("sqlite"):
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "connect_args": {
                "check_same_thread": False,
                "timeout": int(os.getenv("SQL_TIMEOUT", 30)),
            }
        }
    else:
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "connect_args": {
                "timeout": int(os.getenv("SQL_TIMEOUT", 30)),
                "TrustServerCertificate": os.getenv("SQL_TRUST_SERVER_CERTIFICATE", "yes")
            }
        }

    # SQL Alchemy
    db.init_app(app)    
    migrate.init_app(app, db)

    # Vinculación de Extensiones JWT
    # --- NUEVO: CONFIGURACIÓN DE SEGURIDAD PARA SWAGGER ---
    
    if Config.ENV == "development":
        # TODO: Solo para DEV en Swagger.
        app.security_schemes = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Ingresa únicamente tu token de acceso generado en el Login"
            }
        }

        # 🔥 Activa el candado globalmente en Swagger
        app.security = ["BearerAuth"]

        # En desarrollo local permitimos cualquier origen (React, Postman, etc.)
        # CORS(app, resources={r"/*": {"origins": "*"}})
        CORS(
            app, 
            supports_credentials=True,      # Permite el flujo invisible de tus cookies JWT
            resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}} # Aplica solo a tus endpoints de la API
        )
    else:
        # TODO: Cambiar el URL de la app en PRD o QA
        # En producción SOLO permitimos tu dominio real de React
        # Reemplaza con la URL real donde subas tu frontend
        # CORS(app, resources={r"/*": {"origins": ["https://tu-app-react.com", "https://tu-app-react.com"]}})
        CORS(
            app, 
            supports_credentials=True,             # Permite el flujo invisible de tus cookies JWT
            resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173", "https://tu-app-react.com"]}} # Aplica solo a tus endpoints de la API
            # resources={
            #     # Regla 1: Todo lo que esté bajo /api/public/* lo puede consumir cualquier app externa (*)
            #     r"/api/public/*": {
            #         "origins": "*"
            #     },
            #     # Regla 2: Todo lo demás (empleados, asistencia, etc.) es EXCLUSIVO para tu Frontend de React
            #     r"/api/*": {
            #         "origins": ["http://localhost:3000"]
            # }
        )

    jwt.init_app(app)

    # # Configuración de Swagger para documentación de la API
    # swagger_template = {
    #     "swagger": "2.0",
    #     "info": {
    #         "title": "FlaskSQLApp API",
    #         "description": "Documentación Swagger para explorar endpoints del proyecto Flask.",
    #         "version": "1.0.0"
    #     },
    #     "basePath": "/"
    # }
    # swagger_config = {
    #     "headers": [],
    #     "specs": [
    #         {
    #             "endpoint": "apispec_1",
    #             "route": "/apispec_1.json",
    #             "rule_filter": lambda rule: True,
    #             "model_filter": lambda tag: True,
    #         }
    #     ],
    #     "static_url_path": "/flasgger_static",
    #     "swagger_ui": True,
    #     "specs_route": "/apidocs/",
    # }
    # Swagger(app, template=swagger_template, config=swagger_config)

    app.register_blueprint(core_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(leave_application_bp)
    app.register_blueprint(payslip_bp)
    app.register_blueprint(dashboard_bp)

    register_error_handlers(app)
    register_db_handlers(app)
    register_request_context(app)
    register_cache_cleaner(app)
    register_auth_guard(app)

    app.logger.info("Aplicación Flask creada y configurada correctamente.")
    #app.logger.error("Mensaje de error de prueba para verificar configuración de logging.")

    return app

# @app.route('/')
# def index():
#     return 'Hello, World! This is the Flask app running.'


# Expose the app instance 
app = create_app()

# # Punto de entrada de la aplicación
# if __name__ == '__main__':
#     # Ejecutar la aplicación en modo debug
#     app.run(debug=True, use_reloader=False)
