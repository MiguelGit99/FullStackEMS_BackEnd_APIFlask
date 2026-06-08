from flask import Blueprint, jsonify
from apiflask import APIBlueprint

core_bp = APIBlueprint('core', __name__)

@core_bp.route('/healthcheck')
def health():
    """
    Verifica el estado general de la aplicación
    ---
    tags:
      - Core
    responses:
      200:
        description: La aplicación está operativa
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
    """
    return jsonify({'status': 'ok'}), 200
