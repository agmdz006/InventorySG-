# Archivo: app/models/proveedor_model.py
from app import db

class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    nit = db.Column(db.String(20), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    contacto_nombre = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Proveedor {self.nombre}>'