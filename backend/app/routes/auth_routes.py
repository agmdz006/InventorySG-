# Archivo: app/routes/auth_routes.py
from flask import Blueprint, jsonify, request
from app.models.usuario_model import Usuario
from app import db

# Creamos el Blueprint para Autenticación y Usuarios
auth_bp = Blueprint('auth', __name__)

# 1. ENDPOINT PARA LEER (GET): Obtener todos los usuarios
@auth_bp.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    # Viaja a Neon.tech y trae todas las filas como objetos de Python
    usuarios_db = Usuario.query.all()
    
    # Como React no entiende objetos de Python, los convertimos a una lista de diccionarios (JSON)
    lista_usuarios = []
    for usuario in usuarios_db:
        lista_usuarios.append({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "rol": usuario.rol,
            "fecha_creacion": usuario.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify(lista_usuarios), 200


# 2. ENDPOINT PARA CREAR (POST): Insertar un nuevo usuario de prueba
@auth_bp.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    # Recibimos los datos que nos envíe el cliente (o React en el futuro)
    datos = request.get_json()
    
    # Validamos que vengan los datos obligatorios
    if not datos or 'nombre' not in datos or 'correo' not in datos or 'contrasena' not in datos:
        return jsonify({"error": "Faltan datos obligatorios (nombre, correo o contrasena)"}), 400
        
    # Instanciamos nuestro "struct" (Modelo) con la información recibida
    # NOTA: Por ahora guardaremos la contraseña en texto plano, luego le agregaremos encriptación
    nuevo_usuario = Usuario(
        nombre=datos['nombre'],
        correo=datos['correo'],
        contrasena=datos['contrasena'],
        rol=datos.get('rol', 'vendedor') # Si no envían rol, por defecto es vendedor
    )
    
    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return jsonify({
            "mensaje": "¡Usuario creado con éxito en la nube!",
            "usuario_id": nuevo_usuario.id
        }), 201
        
    except Exception as e:
        db.session.rollback() 
        
        # 1. Imprime el error real en tu consola (la pantalla negra)
        print(f"🔥 ERROR EXACTO DE LA BD: {str(e)}") 
        
        # 2. Envía el error real a la pantalla de Postman/Thunder Client
        return jsonify({
            "error": "Hubo un problema al guardar.", 
            "detalle_tecnico": str(e)
        }), 400




#===========ENDPOINTS PARA CLIENTES==============================#

#------Endpoint para crear un cliente-------#
@auth_bp.route('/api/clientes', methods=['POST']) #ruta del endpoint para mandar un cliente a la base de datos
def crear_cliente():
   #Recibimos los datos que nos envía el cliente
   datos = request.get_json()
   #validamos que vengan los campos
   if not datos or 'nombre' not in datos or 'identificacion' not in datos or 'telefono' not in datos or 'correo' not in datos:
    return jsonify({"error", "faltan campos que son necesarios como: nombre, identificacion, telefono o correo"}), 400


   #instanciamos el cliente nuevo
   nuevo_cliente = Cliente(nombre=datos['nombre'], identificacion=datos['identificacion'], telefono=datos['telefono'], correo=datos['correo'])

    #usamos un try para intentar mandar la información y en caso de obtener un error, no crashear el programa
   try:
        db.session.add(nuevo_cliente)
        db.session.commit()


        return jsonify({
            "mensaje": "cliente creado con éxito", 
            "nombre": nuevo_cliente.nombre,
            "identificacion": nuevo_cliente.identificacion,
            "telefono": nuevo_cliente.telefono }), 201



   except Exception as e:
        db.session.rollback()
        print(f"'Error': {str(e)}")
        return jsonify({"error": "Sucedió un error al crear el cliente",
                        "detalle del error": {str(e)}}), 400



#------Endpoint para obtener información de clientes------#
@auth_bp.route('/api/clientes', methods=['GET'])
def get_cliente():
    cliente_db = Cliente.query.all()

    lista_Clientes = []
    for cliente in cliente_db:
        lista_Clientes.append({
            "id": cliente.id,
            "nombre": cliente.nombre,
            "identificacion": cliente.identificacion,
            "telefono": cliente.telefono,
            "correo": cliente.correo
        })

    return jsonify(lista_Clientes), 200




