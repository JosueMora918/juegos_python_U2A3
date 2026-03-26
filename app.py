import logging
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_login import LoginManager, login_required, current_user
from flask_restful import Api
from werkzeug.exceptions import HTTPException, BadRequest, MethodNotAllowed
from models import db, User
import controllers
from api.routes import JuegoList, JuegoResource
from auth import auth as auth_blueprint
app = Flask(__name__)
api = Api(app)

file_handler = logging.FileHandler('errors.log')
file_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_blueprint, url_prefix='/auth')
api.add_resource(JuegoList, '/api/juegos')
api.add_resource(JuegoResource, '/api/juegos/<int:id>')


@app.errorhandler(HTTPException)
def handle_exception(e):
    if request.path.startswith('/api/'):
        return jsonify(code=e.code, name=e.name, description=e.description), e.code

    if e.code == 400:
        return render_template('400.html'), 400
    elif e.code == 404:
        return render_template('404.html'), 404
    elif e.code == 405:
        return render_template('405.html'), 405
    elif e.code == 500:
        return render_template('500.html'), 500

    return render_template('500.html'), 500


@app.route('/error-forzado')
def error_forzado():
    """Ruta para probar el registro de errores en el log (división por cero)"""
    return 1 / 0

@app.route('/')
@login_required
def index():
    juegos = controllers.obtener_juegos()
    return render_template('juegos.html', juegos=juegos)


@app.route('/videogame/<int:id>')
@login_required
def detalle_juego(id):
    if id <= 0:
        app.logger.error(f"Intento de acceso con ID inválido: {id}")
        abort(400)

    juego = controllers.obtener_juego_por_id(id)
    if not juego:
        abort(404)
    return render_template('detalle_juego.html', juego=juego)


@app.route('/agregar')
@login_required
def formulario_agregar_juego():
    return render_template('agregar_juego.html')


@app.route('/guardar', methods=['POST'])
@login_required
def guardar():
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')

    if not nombre or not precio:
        abort(400)  # Bad Request si faltan datos obligatorios

    controllers.insertar_juego(nombre, descripcion, precio)
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
@login_required
def editar(id):
    juego = controllers.obtener_juego_por_id(id)
    if not juego:
        abort(404)
    return render_template('editar_juego.html', juego=juego)


@app.route('/actualizar', methods=['POST'])
@login_required
def actualizar():
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')

    controllers.actualizar_juego(id, nombre, descripcion, precio)
    return redirect(url_for('index'))


@app.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    controllers.eliminar_juego(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=False, port=5000)