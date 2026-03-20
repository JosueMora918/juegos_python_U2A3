from flask import request
from flask_restful import Resource, fields, marshal_with, abort
import controllers  # Importamos tus controladores existentes

# Definimos el formato de salida JSON basado en tu modelo Juego
juego_fields = {
    'id': fields.Integer,
    'nombre': fields.String,
    'descripcion': fields.String,
    'precio': fields.Float
}


class JuegoList(Resource):
    @marshal_with(juego_fields)
    def get(self):
        # GET /api/juegos
        return controllers.obtener_juegos()

    @marshal_with(juego_fields)
    def post(self):
        # POST /api/juegos
        datos = request.get_json()
        if not datos:
            abort(400, message="Faltan datos en formato JSON")

        # Usamos tu controlador para insertar
        controllers.insertar_juego(datos['nombre'], datos['descripcion'], datos['precio'])
        return datos, 201


class JuegoResource(Resource):
    @marshal_with(juego_fields)
    def get(self, id):
        # GET /api/juegos/<id>
        juego = controllers.obtener_juego_por_id(id)
        if not juego:
            abort(404, message=f"Juego con ID {id} no encontrado")
        return juego

    def put(self, id):
        # PUT /api/juegos/<id>
        datos = request.get_json()
        juego_existente = controllers.obtener_juego_por_id(id)
        if not juego_existente:
            abort(404, message="No existe el juego para actualizar")

        # Nota: Usamos el orden de argumentos de tu app.py (id, nombre, desc, precio)
        controllers.actualizar_juego(id, datos['nombre'], datos['descripcion'], datos['precio'])
        return {"message": "Juego actualizado correctamente"}, 200

    def delete(self, id):
        # DELETE /api/juegos/<id>
        juego_existente = controllers.obtener_juego_por_id(id)
        if not juego_existente:
            abort(404, message="El juego no existe o ya fue eliminado")

        controllers.eliminar_juego(id)
        return '', 204