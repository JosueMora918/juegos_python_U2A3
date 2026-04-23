import unittest
import json
from app import app, db
from models import Juego

class APITestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

        j = Juego(nombre='Zelda', descripcion='Aventura', precio=60.00)
        db.session.add(j)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_get_juegos_api(self):
        resp = self.client.get('/api/juegos')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIsInstance(data, list)


if __name__ == '__main__':
    unittest.main()