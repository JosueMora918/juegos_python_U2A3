from flask import Flask, render_template, request, redirect, url_for
from models import db, Juego, User
import controllers
from flask_login import LoginManager, login_required

app = Flask(__name__)
# ¡Importante! Configura una clave secreta para las sesiones y CSRF de los formularios
app.config['SECRET_KEY'] = 'mi_clave_secreta_super_segura_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- Configuración de Flask-Login ---
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Registro del Blueprint ---
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# --- Rutas Protegidas ---
@app.route('/')
@login_required
def index():
    juegos = controllers.obtener_juegos()
    return render_template('juegos.html', juegos=juegos)

@app.route('/guardar', methods=['POST'])
@login_required
def guardar():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    controllers.insertar_juego(nombre, descripcion, precio)
    return redirect(url_for('index'))

@app.route('/agregar')
@login_required
def formulario_agregar_juego():
    return render_template('agregar_juego.html')

@app.route('/editar/<int:id>')
@login_required
def editar(id):
    juego = controllers.obtener_juego_por_id(id)
    return render_template('editar_juego.html', juego=juego)

@app.route('/actualizar', methods=['POST'])
@login_required
def actualizar():
    id = request.form['id']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    controllers.actualizar_juego(id, nombre, descripcion, precio)
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    controllers.eliminar_juego(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)