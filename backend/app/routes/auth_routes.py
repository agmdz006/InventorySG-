from flask import Blueprint, jsonify, request
from app.models.usuario_model import Usuario
from app.models.cliente_model import Cliente
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios_db = Usuario.query.all()
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

@auth_bp.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    datos = request.get_json()
    if not datos or 'nombre' not in datos or 'correo' not in datos or 'contrasena' not in datos:
        return jsonify({"error": "Faltan datos obligatorios (nombre, correo o contrasena)"}), 400
        
    nuevo_usuario = Usuario(
        nombre=datos['nombre'],
        correo=datos['correo'],
        contrasena=datos['contrasena'],
        rol=datos.get('rol', 'vendedor')
    )
    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({"mensaje": "¡Usuario creado con éxito en la nube!", "usuario_id": nuevo_usuario.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Hubo un problema al guardar.", "detalle_tecnico": str(e)}), 400

@auth_bp.route('/api/usuarios/<int:id>', methods=['PUT'])
def editar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
        
    datos = request.get_json()
    usuario.nombre = datos.get('nombre', usuario.nombre)
    usuario.correo = datos.get('correo', usuario.correo)
    usuario.rol = datos.get('rol', usuario.rol)
    if 'contrasena' in datos:
        usuario.contrasena = datos['contrasena']
        
    try:
        db.session.commit()
        return jsonify({"mensaje": f"Usuario {id} actualizado con éxito"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se pudo actualizar el usuario", "detalle": str(e)}), 400

@auth_bp.route('/api/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
        
    try:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"mensaje": f"Usuario {id} eliminado correctamente de la nube"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se puede eliminar el usuario. Puede estar amarrado a transacciones.", "detalle": str(e)}), 400


@auth_bp.route('/api/clientes', methods=['GET'])
def get_clientes():
    clientes_db = Cliente.query.all()
    lista_clientes = []
    for cliente in clientes_db:
        lista_clientes.append({
            "id": cliente.id,
            "nombre": cliente.nombre,
            "identificacion": cliente.identificacion,
            "telefono": cliente.telefono,
            "correo": cliente.correo
        })
    return jsonify(lista_clientes), 200

@auth_bp.route('/api/clientes', methods=['POST'])
def crear_cliente():
    datos = request.get_json()
    if not datos or 'nombre' not in datos or 'identificacion' not in datos or 'telefono' not in datos or 'correo' not in datos:
        return jsonify({"error": "Faltan campos obligatorios: nombre, identificacion, telefono o correo"}), 400

    nuevo_cliente = Cliente(
        nombre=datos['nombre'],
        identificacion=datos['identificacion'],
        telefono=datos['telefono'],
        correo=datos['correo']
    )
    try:
        db.session.add(nuevo_cliente)
        db.session.commit()
        return jsonify({
            "mensaje": "Cliente creado con éxito", 
            "id": nuevo_cliente.id,
            "nombre": nuevo_cliente.nombre
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Sucedió un error al crear el cliente", "detalle": str(e)}), 400

@auth_bp.route('/api/clientes/<int:id>', methods=['PUT'])
def editar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    datos = request.get_json()
    cliente.nombre = datos.get('nombre', cliente.nombre)
    cliente.identificacion = datos.get('identificacion', cliente.identificacion)
    cliente.telefono = datos.get('telefono', cliente.telefono)
    cliente.correo = datos.get('correo', cliente.correo)
    
    try:
        db.session.commit()
        return jsonify({"mensaje": f"Cliente {id} actualizado con éxito"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se pudo actualizar el cliente", "detalle": str(e)}), 400

@auth_bp.route('/api/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
        
    try:
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({"mensaje": f"Cliente {id} eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se puede eliminar el cliente. Puede tener historial de ventas.", "detalle": str(e)}), 400