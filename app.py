from flask import Flask, jsonify, send_file, send_from_directory
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

app.register_blueprint(auth)

class ContenidoExtra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)

@app.route('/<filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

@app.route('/')
@app.route('/index.html')
def home():
    return send_file('index.html')

@app.route('/login.html')
def login_page():
    return send_file('login.html')

@app.route('/registro.html')
def registro_page():
    return send_file('registro.html')

@app.route('/api/navigationmenu')
def navigation_menu():
    connection = pymysql.connect(
        host="maglev.proxy.rlwy.net",
        user="root",
        password="TU_CONTRASEÑA",
        database="railway",
        port=11363,
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM navigationmenu ORDER BY display_order ASC")
        menu = cursor.fetchall()
    return jsonify(menu)

@app.route('/api/contenidoextra')
def contenido_extra():
    extras = ContenidoExtra.query.all()
    return jsonify([{'name': x.name, 'link': x.link} for x in extras])

# 📦 Función para importar base de datos desde localiglesia.sql
def importar_sql():
    connection = pymysql.connect(
        host="maglev.proxy.rlwy.net",
        user="root",
        password="YyaSmXgtoWMVgJBofmHVznfteoMihXwb",
        database="railway",
        port=11363,
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )

    with open("localiglesia.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    with connection.cursor() as cursor:
        for statement in sql_script.split(";"):
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                except Exception as e:
                    print(f"❌ Error ejecutando: {statement}\n{e}")

    print("✅ Tablas importadas exitosamente.")

if __name__ == '__main__':
    # ⚠️ Descomenta la siguiente línea solo una vez para importar la base de datos
    # importar_sql()
    app.run(host="0.0.0.0", port=10000)
