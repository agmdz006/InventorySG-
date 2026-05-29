# Archivo: run.py
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    # El servidor correrá en el puerto 5000 por defecto
    app.run(debug=True)