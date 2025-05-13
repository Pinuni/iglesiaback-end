from flask import Flask, jsonify, send_from_directory, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os
from authroutes import auth

# Inicializar la app
app = Flask(__name__)

# CORS para frontend de Netlify o dominio personalizado
CORS(app, resources={r"/*": {"origins": ["https://iglesiarefugioquebs.site"]}}, supports_credentials=True)

# Configuración de SQLAlchemy (aunque no estás usando muchos modelos)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:YyaSmXgtoWMVgJBofmHVznfteoMihXwb@maglev.proxy.rlwy.net:11363/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Registrar Blueprint con rutas de auth (registro/login)
app.register_blueprint(auth)

# Modelo de ejemplo para sección "contenido extra"
class ContenidoExtra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)

# Redirección al sitio principal
@app.route('/')
def home():
    return redirect("https://iglesiarefugioquebs.site")

# Ruta para servir archivos (por si cargas imágenes u otros en el futuro)
@app.route('/<filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

# API: Devuelve el contenido extra desde la tabla
@app.route('/api/contenidoextra')
def contenido_extra():
    extras = ContenidoExtra.query.all()
    return jsonify([{'name': x.name, 'link': x.link} for x in extras])

# API: Devuelve el menú de navegación desde la tabla navigationmenu
@app.route('/api/navigationmenu')
def navigation_menu():
    connection = pymysql.connect(
        host="maglev.proxy.rlwy.net",
        user="root",
        password="YyaSmXgtoWMVgJBofmHVznfteoMihXwb",
        database="railway",
        port=11363,
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM navigationmenu ORDER BY display_order ASC")
        menu = cursor.fetchall()
    return jsonify(menu)

# Iniciar servidor
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
