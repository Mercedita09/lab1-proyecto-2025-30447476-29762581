import _mysql_connector
def conectar():
    conexion = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='api_gestion_medica_lab1' 
    )
    return conexion