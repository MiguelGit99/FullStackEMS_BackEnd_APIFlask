import logging
from flask import jsonify
from apiflask import APIBlueprint
from blueprints.products.models import Product
from blueprints.products.services import get_all_brands, get_all_products
from blueprints.products.schemas import BrandSchema, ProductSchema

logger = logging.getLogger(__name__)

products_bp = APIBlueprint('products', 
                        __name__,
                        url_prefix='/api/products')

# @products_bp.route('/', methods=['GET'])
@products_bp.get('/')
@products_bp.output(list[ProductSchema], status_code=200)
def get_products():
    """
    Obtiene la lista de productos usando la capa de services.py
    ---
    tags:
      - Products
    responses:
      200:
        description: Lista de productos obtenida exitosamente
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: Producto A
              price:
                type: number
                format: float
                example: 19.99
    """
    logger.info("Obteniendo lista de productos")

    # products = get_all_products()
    # #return jsonify([{"id": p.product_id, "name": p.product_name, "price": float(p.list_price)} for p in products])
    
    # serialized_products = [
    #     ProductSchema.model_validate(p).model_dump(mode='json') # mode-json ayuda a serializar correctamente Decimal, datetime, UUID y otros tipos especiales
    #     for p in products
    # ]

    # return jsonify(serialized_products), 200
    return get_all_products()


# @products_bp.route('/brands', methods=['GET'])
@products_bp.get('/brands')
@products_bp.output(list[BrandSchema], status_code=200)
def get_brands():
    """
    Obtiene la lista de marcas usando la capa de services.py
    ---
    tags:
      - Products
    responses:
      200:
        description: Lista de marcas obtenida exitosamente
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: Marca A
    """
    logger.info("Obteniendo lista de marcas")
    # brands = get_all_brands()
    # # return jsonify([{"id": p.product_id, "name": p.product_name, "price": float(p.list_price)} for p in products])
    
    # serialized_brands = [
    #     BrandSchema.model_validate(b).model_dump()
    #     for b in brands
    # ]

    # return jsonify(serialized_brands), 200
    return get_all_brands()
    