# from flask import Blueprint, jsonify

from blueprints.products.models import Brand, Product

# products_bp = Blueprint('products', 
#                         __name__,
#                         url_prefix='/products')

# @products_bp.route('/', methods=['GET'])
# def get_products():
#     """
#     Obtiene la lista de productos
#     ---
#     tags:
#       - Products
#     responses:
#       200:
#         description: Lista de productos obtenida exitosamente
#         schema:
#           type: array
#           items:
#             type: object
#             properties:
#               id:
#                 type: integer
#                 example: 1
#               name:
#                 type: string
#                 example: Producto A
#               price:
#                 type: number
#                 format: float
#                 example: 19.99
#     """
#     # Aquí iría la lógica para obtener los productos desde la base de datos
#     sample_products = [
#         {"id": 1, "name": "Producto A", "price": 19.99},
#         {"id": 2, "name": "Producto B", "price": 29.99}
#     ]
#     return jsonify(sample_products), 200

# def get_product_by_id(product_id):
#     """
#     Obtiene un producto por su ID
#     ---
#     tags:
#       - Products
#     parameters:
#       - name: product_id
#         in: path
#         type: integer
#         required: true
#     responses:
#       200:
#         description: Producto obtenido exitosamente
#         schema:
#           type: object
#           properties:
#             id:
#               type: integer
#               example: 1
#             name:
#               type: string
#               example: Producto A
#             price:
#               type: number
#               format: float
#               example: 19.99
#       404:
#         description: Producto no encontrado
#     """
#     # Aquí iría la lógica para obtener el producto desde la base de datos por su ID
#     if product_id == 1:
#         return jsonify({"id": 1, "name": "Producto A", "price": 19.99}), 200
#     else:
#         return jsonify({"error": "Producto no encontrado"}), 404
    
from blueprints.products.models import Product


def get_all_products():
    """
    Obtiene todos los productos
    ---
    tags:
      - Products
    responses:
      200: 
          description: Todos los productos obtenidos exitosamente
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
    # Aquí iría la lógica para obtener todos los productos desde la base de datos
    # sample_products = [
    #     {"id": 1, "name": "Producto A", "price": 19.99},
    #     {"id": 2, "name": "Producto B", "price": 29.99}
    # ]

    products = Product.query.all()
    return products
    # products_list = [{"id": p.product_id, "name": p.product_name, "price": float(p.list_price)} for p in products]
    # return jsonify(products_list), 200

    # return jsonify(sample_products), 200    


def get_all_brands():
    brands = Brand.query.all()
    
    return [
        {
            "brand_id": b.brand_id,
            "brand_name": b.brand_name
        }
        for b in brands
    ]