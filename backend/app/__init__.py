# Archivo: app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Creamos la instancia de la base de datos (vacía por ahora)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Conectamos la base de datos con nuestra app Flask
    db.init_app(app)

    # Aquí registraremos las rutas (Controladores) más adelante

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    
    from app.routes.inventario_routes import inventario_bp
    app.register_blueprint(inventario_bp)
    
    return app