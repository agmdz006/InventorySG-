# Archivo: app/routes/inventario_routes.py
from flask import Blueprint, jsonify, request
from app.models.proveedor_model import Proveedor
from app.models.producto_model import Producto
from app import db

inventario_bp = Blueprint('inventario', __name__)

# ==============================================================================
# CRUD DE PROVEEDORES
# ==============================================================================

@inventario_bp.route('/api/proveedores', methods=['GET'])
def obtener_proveedores():
    proveedores_db = Proveedor.query.all()
    lista = []
    for prov in proveedores_db:
        lista.append({
            "id": prov.id,
            "nombre": prov.nombre,
            "nit": prov.nit,
            "telefono": prov.telefono,
            "direccion": prov.direccion,
            "contacto_nombre": prov.contacto_nombre
        })
    return jsonify(lista), 200

@inventario_bp.route('/api/proveedores', methods=['POST'])
def crear_proveedor():
    datos = request.get_json()
    campos_obligatorios = ['nombre', 'nit', 'telefono', 'direccion', 'contacto_nombre']
    if not datos or not all(k in datos for k in campos_obligatorios):
        return jsonify({"error": "Faltan campos obligatorios para el proveedor"}), 400

    nuevo_prov = Proveedor(
        nombre=datos['nombre'],
        nit=datos['nit'],
        telefono=datos['telefono'],
        direccion=datos['direccion'],
        contacto_nombre=datos['contacto_nombre']
    )
    try:
        db.session.add(nuevo_prov)
        db.session.commit()
        return jsonify({"mensaje": "Proveedor creado con éxito", "id": nuevo_prov.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se pudo crear el proveedor", "detalle": str(e)}), 400

@inventario_bp.route('/api/proveedores/<int:id>', methods=['PUT'])
def editar_proveedor(id):
    prov = Proveedor.query.get(id)
    if not prov:
        return jsonify({"error": "Proveedor no encontrado"}), 404
    
    datos = request.get_json()
    prov.nombre = datos.get('nombre', prov.nombre)
    prov.nit = datos.get('nit', prov.nit)
    prov.telefono = datos.get('telefono', prov.telefono)
    prov.direccion = datos.get('direccion', prov.direccion)
    prov.contacto_nombre = datos.get('contacto_nombre', prov.contacto_nombre)
    
    try:
        db.session.commit()
        return jsonify({"mensaje": f"Proveedor {id} actualizado con éxito"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se pudo actualizar", "detalle": str(e)}), 400

@inventario_bp.route('/api/proveedores/<int:id>', methods=['DELETE'])
def eliminar_proveedor(id):
    prov = Proveedor.query.get(id)
    if not prov:
        return jsonify({"error": "Proveedor no encontrado"}), 404
    try:
        db.session.delete(prov)
        db.session.commit()
        return jsonify({"mensaje": f"Proveedor {id} eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se puede eliminar. Puede tener productos asociados.", "detalle": str(e)}), 400


# ==============================================================================
# CRUD DE PRODUCTOS (CONTROL DE INVENTARIO)
# ==============================================================================

@inventario_bp.route('/api/productos', methods=['GET'])
def obtener_productos():
    productos_db = Producto.query.all()
    lista = []
    for prod in productos_db:
        lista.append({
            "id": prod.id,
            "codigo_barras": prod.codigo_barras,
            "nombre": prod.nombre,
            "precio_compra": float(prod.precio_compra), # Conversión a float para JSON
            "precio_venta": float(prod.precio_venta),
            "stock_actual": prod.stock_actual,
            "stock_minimo": prod.stock_minimo,
            "proveedor_id": prod.proveedor_id
        })
    return jsonify(lista), 200

@inventario_bp.route('/api/productos', methods=['POST'])
def crear_producto():
    datos = request.get_json()
    campos_obligatorios = ['codigo_barras', 'nombre', 'precio_compra', 'precio_venta', 'proveedor_id']
    if not datos or not all(k in datos for k in campos_obligatorios):
        return jsonify({"error": "Faltan campos obligatorios para el producto"}), 400

    # VALIDACIÓN DE INGENIERÍA: Verificar si el proveedor realmente existe en la nube
    proveedor_existe = Proveedor.query.get(datos['proveedor_id'])
    if not proveedor_existe:
        return jsonify({"error": f"El proveedor_id {datos['proveedor_id']} no existe en la base de datos. Créalo primero."}), 400

    nuevo_prod = Producto(
        codigo_barras=datos['codigo_barras'],
        nombre=datos['nombre'],
        precio_compra=datos['precio_compra'],
        precio_venta=datos['precio_venta'],
        stock_actual=datos.get('stock_actual', 0), # Si no lo envían, empieza en 0
        stock_minimo=datos.get('stock_minimo', 5),
        proveedor_id=datos['proveedor_id']
    )
    try:
        db.session.add(nuevo_prod)
        db.session.commit()
        return jsonify({"mensaje": "Producto guardado con éxito en el inventario", "id": nuevo_prod.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se pudo registrar el producto", "detalle": str(e)}), 400

@inventario_bp.route('/api/productos/<int:id>', methods=['PUT'])
def editar_producto(id):
    prod = Producto.query.get(id)
    if not prod:
        return jsonify({"error": "Producto no encontrado"}), 404
    
    datos = request.get_json()
    
    # Si van a cambiar el proveedor, validamos que el nuevo también exista
    if 'proveedor_id' in datos:
        if not Proveedor.query.get(datos['proveedor_id']):
            return jsonify({"error": "El nuevo proveedor_id no existe"}), 400
        prod.proveedor_id = datos['proveedor_id']

    prod.codigo_barras = datos.get('codigo_barras', prod.codigo_barras)
    prod.nombre = datos.get('nombre', prod.nombre)
    prod.precio_compra = datos.get('precio_compra', prod.precio_compra)
    prod.precio_venta = datos.get('precio_venta', prod.precio_venta)
    prod.stock_actual = datos.get('stock_actual', prod.stock_actual)
    prod.stock_minimo = datos.get('stock_minimo', prod.stock_minimo)
    
    try:
        db.session.commit()
        return jsonify({"mensaje": f"Producto {id} modificado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se pudo actualizar el producto", "detalle": str(e)}), 400

@inventario_bp.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    prod = Producto.query.get(id)
    if not prod:
        return jsonify({"error": "Producto no encontrado"}), 404
    try:
        db.session.delete(prod)
        db.session.commit()
        return jsonify({"mensaje": f"Producto {id} eliminado del sistema"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se puede borrar el producto. Puede tener historial de ventas o compras.", "detalle": str(e)}), 400