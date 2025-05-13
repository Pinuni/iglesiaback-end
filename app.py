from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pymysql
from authroutes import auth

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://iglesiarefugioquebs.site"]}}, supports_credentials=True)

# Configuración de base de datos 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://iglesiar_ken:HijoDeDios1@17@sql201.byetcluster.com/iglesiar_localiglesia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Registrar blueprint de autenticación
app.register_blueprint(auth)

# Modelo opcional para contenido extra
class ContenidoExtra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)

# Ruta principal
@app.route('/')
def home():
    return jsonify({"message": "Backend API activa y funcionando correctamente ✅"}), 200

# API para el menú de navegación
@app.route('/api/navigationmenu')
def navigation_menu():
    connection = pymysql.connect(
        host="sql201.byetcluster.com",
        user="iglesiar_kenito",
        password="HijoDeDios1@17",
        database="iglesiar_localiglesia",
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM navigationmenu ORDER BY display_order ASC")
        menu = cursor.fetchall()
    return jsonify(menu)

# API para contenido adicional dinámico
@app.route('/api/contenidoextra')
def contenido_extra():
    extras = ContenidoExtra.query.all()
    return jsonify([{'name': x.name, 'link': x.link} for x in extras])

# Ejecutar app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
