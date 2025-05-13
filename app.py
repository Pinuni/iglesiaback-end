from flask import Flask, jsonify, send_from_directory, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os
from authroutes import auth

# Inicializar la app de Flask
app = Flask(__name__)

# Habilitar CORS para permitir peticiones desde el frontend en Netlify o dominio personalizado
CORS(app, resources={r"/*": {"origins": ["https://iglesiarefugioquebs.site"]}}, supports_credentials=True)

# Configuración de SQLAlchemy (aunque solo estás usando un modelo)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:YyaSmXgtoWMVgJBofmHVznfteoMihXwb@maglev.proxy.rlwy.net:11363/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Registrar las rutas de autenticación (registro/login)
app.register_blueprint(auth)

# Modelo: contenido extra dinámico para la página
class ContenidoExtra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)

# Redireccionar a tu página principal al acceder a "/"
@app.route('/')
def home():
    return redirect("https://iglesiarefugioquebs.site")

# Servir archivos directamente desde el directorio actual (ej: imágenes o PDFs)
@app.route('/<filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

# API: contenido extra (ej: enlaces adicionales dinámicos en el menú)
@app.route('/api/contenidoextra')
def contenido_extra():
    extras = ContenidoExtra.query.all()
    return jsonify([{'name': x.name, 'link': x.link} for x in extras])

# API: menú de navegación cargado desde base de datos
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

# Iniciar servidor localmente o en plataforma como Render
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
