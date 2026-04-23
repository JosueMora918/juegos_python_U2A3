import unittest
from app import app, db
from models import Juego

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_juego_creation(self):
        j = Juego(nombre='Mario Bros', descripcion='Plataformas', precio=59.99)
        db.session.add(j)
        db.session.commit()
        self.assertEqual(Juego.query.count(), 1)


if __name__ == '__main__':
    unittest.main()