import os
import sys
from app import create_app

app = create_app()

# # Punto de entrada de la aplicación (con python)
if __name__ == "__main__":
    app.run(host=os.getenv('FLASK_RUN_HOST', '127.0.0.1'), port=int(os.getenv('FLASK_RUN_PORT', 5000)))