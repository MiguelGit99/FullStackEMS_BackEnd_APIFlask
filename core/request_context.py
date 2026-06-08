from flask import g, request
from uuid import uuid4
from core.extensions import db


def register_request_context(app):

    @app.before_request
    def before_request():
        g.request_id = request.headers.get(
            "X-Request-ID",
            str(uuid4())
        )

# Limpia cache en queries a SQL Server en metodos GET y HEAD
def register_cache_cleaner(app):
    @app.before_request
    def clean_cache_on_queries():
        # 🟢 Si la petición es de solo lectura (GET), vaciamos la caché acumulada
        if request.method in ["GET", "HEAD"]:
            db.session.expire_all() 
            # expire_all() no destruye la sesión, solo marca todos los objetos 
            # en memoria como "viejos" para que SQLAlchemy consulte la BD obligatoriamente.
