import pymysql

# Se llama DB porque usamos docker en vez de xampp, regresar a localhost luego

def obtener_conexion():
    return pymysql.connect(host='db',
                                user='root',
                                password='root',
                                db='juegos')