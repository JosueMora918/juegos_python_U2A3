from models import db, Juego

def obtener_juegos():
    # Retorna todos los registros de la tabla juegos
    return Juego.query.all()

def obtener_juego_por_id(id):
    # Retorna un juego específico basado en su llave primaria
    return Juego.query.get(id)

def insertar_juego(nombre, descripcion, precio):
    # Crea una nueva instancia del modelo y la guarda
    nuevo_juego = Juego(nombre=nombre, descripcion=descripcion, precio=precio)
    db.session.add(nuevo_juego)
    db.session.commit()

def actualizar_juego(id, nombre, descripcion, precio):
    # Obtiene el juego, modifica sus atributos y guarda los cambios
    juego = obtener_juego_por_id(id)
    if juego:
        juego.nombre = nombre
        juego.descripcion = descripcion
        juego.precio = precio
        db.session.commit()

def eliminar_juego(id):
    # Obtiene el juego y lo elimina de la sesión
    juego = obtener_juego_por_id(id)
    if juego:
        db.session.delete(juego)
        db.session.commit()