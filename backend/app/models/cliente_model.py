from app import db 
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    identificacion = db.Column(db.String(20), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(150), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Cliente {self.nombre} - {self.telefono}>'

