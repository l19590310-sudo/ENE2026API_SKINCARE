import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear instancia de Flask
app = Flask(__name__)

# Configuración de PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# Modelo de la Base de Datos
# =========================
class ProductoSkincare(db.Model):
    __tablename__ = 'productos_skincare'

    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    marca = db.Column(db.String(100))
    tipo_producto = db.Column(db.String(50))
    tipo_piel = db.Column(db.String(50))
    precio = db.Column(db.Numeric(8, 2))


# =========================
# Obtener todos los productos
# =========================
@app.route('/productos', methods=['GET'])
def get_productos():
    productos = ProductoSkincare.query.all()
    lista_productos = []

    for producto in productos:
        lista_productos.append({
            'id_producto': producto.id_producto,
            'nombre': producto.nombre,
            'marca': producto.marca,
            'tipo_producto': producto.tipo_producto,
            'tipo_piel': producto.tipo_piel,
            'precio': float(producto.precio) if producto.precio else None
        })

    return jsonify(lista_productos)


# =========================
# Obtener un producto por ID
# =========================
@app.route('/productos/<int:id_producto>', methods=['GET'])
def get_producto(id_producto):
    producto = ProductoSkincare.query.get(id_producto)

    if producto is None:
        return jsonify({'msg': 'Producto no encontrado'})

    return jsonify({
        'id_producto': producto.id_producto,
        'nombre': producto.nombre,
        'marca': producto.marca,
        'tipo_producto': producto.tipo_producto,
        'tipo_piel': producto.tipo_piel,
        'precio': float(producto.precio) if producto.precio else None
    })


# =========================
# Crear nuevo producto
# =========================
@app.route('/productos', methods=['POST'])
def create_producto():
    data = request.get_json()

    nuevo_producto = ProductoSkincare(
        nombre=data.get('nombre'),
        marca=data.get('marca'),
        tipo_producto=data.get('tipo_producto'),
        tipo_piel=data.get('tipo_piel'),
        precio=data.get('precio')
    )

    db.session.add(nuevo_producto)
    db.session.commit()

    return jsonify({'msg': 'Producto creado correctamente'})


# =========================
# Actualizar producto
# =========================
@app.route('/productos/<int:id_producto>', methods=['PUT'])
def update_producto(id_producto):
    producto = ProductoSkincare.query.get(id_producto)

    if producto is None:
        return jsonify({'msg': 'Producto no encontrado'})

    data = request.get_json()

    if "nombre" in data:
        producto.nombre = data['nombre']
    if "marca" in data:
        producto.marca = data['marca']
    if "tipo_producto" in data:
        producto.tipo_producto = data['tipo_producto']
    if "tipo_piel" in data:
        producto.tipo_piel = data['tipo_piel']
    if "precio" in data:
        producto.precio = data['precio']

    db.session.commit()
    return jsonify({'msg': 'Producto actualizado correctamente'})


# =========================
# Eliminar producto
# =========================
@app.route('/productos/<int:id_producto>', methods=['DELETE'])
def delete_producto(id_producto):
    producto = ProductoSkincare.query.get(id_producto)

    if producto is None:
        return jsonify({'msg': 'Producto no encontrado'})

    db.session.delete(producto)
    db.session.commit()

    return jsonify({'msg': 'Producto eliminado correctamente'})


# Ejecutar app
if __name__ == '__main__':
    app.run(debug=True)