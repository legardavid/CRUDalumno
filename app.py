from distutils.command.config import config
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app =Flask(__name__)

app.config.from_object('config.DevelopmentConfig')

conexion=MySQL(app)

@app.route('/alumno', methods=['GET'])  #lista los alumnos
def listaralumno():
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT cedula, nombre, edad FROM alumno"
        cursor.execute(sql)
        datos = cursor.fetchall() #convierte la respuesta en datos entendibles para Py
        informacion=[]
        #print(datos) para verificar en consola

        for fila in datos:
            info={'cedula':fila[0],'nombre':fila[1],'edad':fila[2]} #crea un diccionario para poder generar el JSON
            informacion.append(info)
        return jsonify({'informacion':informacion, 'mensaje':"Alumnos listados"})
    except Exception as ex:
         return jsonify({'mensaje': "Error"})

@app.route('/alumno/<cedula>', methods=['GET']) #lista solo un alumno con <cedula> parametro de busqueda por URL
def leercedula(cedula):
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT cedula, nombre, edad FROM alumno WHERE cedula = '{0}'".format(cedula) #{0} parametro que va a buscar en sql recibido por url
        cursor.execute(sql)
        datos = cursor.fetchone() #por que solo vamos a tener una sola respuesta
        #print(datos) #para verificar en consola
        
        if datos != None:
            info={'cedula':datos[0],'nombre':datos[1],'edad':datos[2]} #crea un diccionario indivudial para poder generar el JSON
            return jsonify({'Alumno':info, 'mensaje':"Alumnos Encontrado"})
        else:
            return jsonify({'mensaje':"Alumnos no encontrado, pruebe con otra cedula"})
    except Exception as ex:
         return jsonify({'mensaje': "Error"})

@app.route('/alumno', methods=['POST'])  #agregar los alumnos
def registaralumno():
    try:
        #print(request.json) # probar el objeto de la peticion
        cursor = conexion.connection.cursor()
        sql="""INSERT INTO alumno (cedula, nombre, edad) 
        VALUES ('{0}','{1}',{2})""".format(request.json['cedula'],request.json['nombre'],request.json['edad']) #Consula SQL para insertar datos por medio de request
        cursor.execute(sql)
        conexion.connection.commit() # Confirma la accion de registro
        return jsonify({'Mensaje':"Alumnos registrados."})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@app.route('/alumno/<cedula>', methods=['DELETE']) #Borra alumno  <cedula> parametro de busqueda por URL
def borraralumno(cedula):
    try:
        cursor = conexion.connection.cursor()
        sql= "DELETE FROM alumno WHERE cedula = '{0}'".format(cedula)
        cursor.execute(sql)
        conexion.connection.commit() # Confirma la accion de registro
        return jsonify({'Mensaje':"Alumno eliminado."})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@app.route('/alumno/<cedula>', methods=['PUT']) #Actualiza alumno  <cedula> parametro de busqueda por URL
def Actualizaralumno(cedula):
    try:
        cursor = conexion.connection.cursor()
        sql= """UPDATE alumno SET nombre = '{0}', edad = {1} 
        WHERE cedula ='{2}'""".format(request.json['nombre'],request.json['edad'],cedula)
        cursor.execute(sql)
        conexion.connection.commit() # Confirma la accion de registro
        return jsonify({'Mensaje':"Alumno actualizado."})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

def pagina_no_encontrada(error):
    return "<h1> La pagina a la que intentas acceder no existe. </h1>"

if __name__=='__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()