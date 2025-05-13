from flask import Flask, jsonify, send_from_directory, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os
from authroutes import auth

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://iglesiarefugioquebs.site"]}}, supports_credentials=True)

# Configuración de base de datos Railway
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:YyaSmXgtoWMVgJBofmHVznfteoMihXwb@maglev.proxy.rlwy.net:11363/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Registro de blueprint
app.register_blueprint(auth)

# Modelo de ejemplo
class ContenidoExtra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)

# Redirección a tu sitio oficial
@app.route('/')
def home():
    return redirect("https://iglesiarefugioquebs.site")

# Endpoint para archivos (si algún día subes imágenes u otros)
@app.route('/<filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

# Endpoint para contenido extra
@app.route('/api/contenidoextra')
def contenido_extra():
    extras = ContenidoExtra.query.all()
    return jsonify([{'name': x.name, 'link': x.link} for x in extras])

# Endpoint para navegación (menú)
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
