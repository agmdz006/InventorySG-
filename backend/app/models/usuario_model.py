# Archivo: app/models/usuario_model.py
from app import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuarios' # Debe llamarse EXACTAMENTE igual que en tu base de datos

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False, default='vendedor')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Esto es solo para que al imprimir el usuario en la consola, se lea bonito
    def __repr__(self):
        return f'<Usuario {self.nombre} - {self.rol}>'