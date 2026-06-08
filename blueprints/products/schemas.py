# Usando Schemas con Pydantic para validar y serializar datos de productos y marcas
# Schemas se usa para los modelos de datos entre el FronEnd y el BackEnd, mientras que los Models se usan para la representación de la base de datos
# Esto ayuda a mantener el código limpio y a manejar correctamente tipos de datos complejos como Decimal
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class BrandSchema(BaseModel):
    brand_id: int
    brand_name: str

    model_config = ConfigDict(from_attributes=True)


class ProductSchema(BaseModel):
    product_id: int
    product_name: str
    brand_id: int
    category_id: int
    model_year: int
    list_price: Decimal

    model_config = ConfigDict(from_attributes=True)