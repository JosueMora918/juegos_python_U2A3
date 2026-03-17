from app import app
from models import db, User

with app.app_context():
    # 1. Borramos la tabla de usuarios actual (esto no afecta a tus juegos)
    User.__table__.drop(db.engine)

    # 2. La volvemos a crear con el nuevo límite de 255
    db.create_all()

    # 3. Creamos al usuario de nuevo
    nuevo_usuario = User(username='admin')
    nuevo_usuario.password = 'secreto123'
    db.session.add(nuevo_usuario)
    db.session.commit()

    print("¡Tabla corregida y usuario creado!")