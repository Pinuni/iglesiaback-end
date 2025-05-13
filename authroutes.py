from flask import Blueprint, request, jsonify, redirect
import pymysql
from datetime import datetime
from flask_cors import CORS

# Crear Blueprint
auth = Blueprint('auth', __name__)
CORS(auth, resources={r"/*": {"origins": ["https://iglesiarefugioquebs.site"]}}, supports_credentials=True)

# Conexión a base de datos (Railway)
def get_connection():
    return pymysql.connect(
        host="maglev.proxy.rlwy.net",
        user="root",
        password="YyaSmXgtoWMVgJBofmHVznfteoMihXwb",
        database="railway",
        port=11363,
        cursorclass=pymysql.cursors.DictCursor
    )

# REGISTRO
@auth.route('/registro', methods=['POST'])
def registrar_usuario():
    username = request.form.get('nombre')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    print("📥 Nombre:", username)
    print("📥 Email:", email)
    print("📥 Password:", password)
    print("📥 Confirm:", confirm_password)

    if not all([username, email, password, confirm_password]):
        return jsonify({'message': 'Todos los campos son obligatorios'}), 400

    if password != confirm_password:
        return jsonify({'message': 'Las contraseñas no coinciden'}), 400

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
                if cursor.fetchone():
                    return jsonify({'message': 'El usuario ya existe'}), 400

                cursor.execute(
                    "INSERT INTO usuarios (username, email, password, created_at) VALUES (%s, %s, %s, %s)",
                    (username, email, password, datetime.now())
                )
                connection.commit()
                print("✅ Usuario registrado:", email)
                return jsonify({'success': True, 'redirect': 'https://iglesiarefugioquebs.site/login.html'})


    except Exception as e:
        import traceback
        print("🔥 Error al registrar:", e)
        traceback.print_exc()
        return jsonify({'message': 'Error interno del servidor'}), 500

# LOGIN
@auth.route('/login', methods=['POST'])
def login_usuario():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
                user = cursor.fetchone()
                print("🔎 Usuario encontrado:", user)

                if not user:
                    return jsonify({'message': 'Correo no registrado'}), 400

                if user['password'] != password:
                    return jsonify({'message': 'Contraseña incorrecta'}), 400

                print("✅ Login exitoso:", email)
                return jsonify({'success': True, 'redirect': 'https://iglesiarefugioquebs.site/index.html'})


    except Exception as e:
        import traceback
        print("🔥 Error al iniciar sesión:", e)
        traceback.print_exc()
        return jsonify({'message': 'Error interno del servidor'}), 500
