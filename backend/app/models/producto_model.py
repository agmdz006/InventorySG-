# Archivo: app/models/producto_model.py
from app import db

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    codigo_barras = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    # db.Numeric(10,2) es ideal para dinero, evita errores de redondeo de los floats
    precio_compra = db.Column(db.Numeric(10, 2), nullable=False)
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False)
    stock_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=5)
    
    # Clave Foránea: Vincula el producto con un proveedor existente
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)

    def __repr__(self):
        return f'<Producto {self.nombre} - Stock: {self.stock_actual}>'