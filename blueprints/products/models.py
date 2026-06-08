from core.extensions import db

class Product(db.Model):
    __tablename__ = 'products'

    #__table_args__ = {"schema": "production"}
    
    product_id = db.Column(db.INT, primary_key=True)
    product_name = db.Column(db.VARCHAR(255), nullable=False)
    brand_id = db.Column(db.INT, nullable=False)
    category_id = db.Column(db.INT, nullable=False)
    model_year = db.Column(db.SMALLINT, nullable=False)
    list_price = db.Column(db.DECIMAL(10, 2), nullable=False)

    def __repr__(self):
        return f'<Product {self.product_id}-{self.product_name}>'

class Brand(db.Model):
    __tablename__ = 'brands'
    
    brand_id = db.Column(db.INT, primary_key=True)
    brand_name = db.Column(db.VARCHAR(255), nullable=False)
    
    def __repr__(self):
        return f'<Brand {self.brand_id}-{self.brand_name}>'
        