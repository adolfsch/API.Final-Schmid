from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import hashlib
from datetime import datetime 


class Tarea:
    def __init__(self, titulo, descripcion, estado='pendiente', creada=None, actualizada=None):
        self.titulo = titulo
        self.descripcion = descripcion
        self.estado = estado
        self.creada = creada or datetime.now()
        self.actualizada = actualizada or datetime.now()

class Persona:    #ESTA CLASE VA A ALMACENAR LA PERSONA DENTRO DE LA BASE DE DATOS
    def __init__(self, nombre, contraseña):
        self.nombre = nombre
        self.contraseña = contraseña

class AdminTarea:
    def __init__(self, db_path):       #Preparativos SQLITE 
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._crear_tabla_tareas()
        self._crear_tabla_personas()

    def _crear_tabla_tareas(self):
        query = '''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            descripcion TEXT,
            estado TEXT,
            creada TEXT,
            actualizada TEXT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

    def _crear_tabla_personas(self):
        query = '''
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            contraseña TEXT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

    def agregar_tarea(self, tarea):
        query = '''
        INSERT INTO tareas (titulo, descripcion, estado, creada, actualizada)
        VALUES (?, ?, ?, ?, ?)
        '''
        values = (
            tarea.titulo,
            tarea.descripcion,
            tarea.estado,
            tarea.creada.isoformat(),
            tarea.actualizada.isoformat()
        )
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor.lastrowid

    def traer_tarea(self, tarea_id):
        query = '''
        SELECT * FROM tareas WHERE id = ?
        '''
        self.cursor.execute(query, (tarea_id,))
        tarea_data = self.cursor.fetchone()
        if tarea_data:
            tarea = Tarea(
                tarea_data[1],
                tarea_data[2],
                tarea_data[3],
                datetime.fromisoformat(tarea_data[4]),
                datetime.fromisoformat(tarea_data[5])
            )
            return tarea
        return None

    def actualizar_estado_tarea(self, tarea_id, estado):
        query = '''
        UPDATE tareas SET estado = ?, actualizada = ? WHERE id = ?
        '''
        values = (
            estado,
            datetime.now().isoformat(),
            tarea_id
        )
        self.cursor.execute(query, values)
        self.conn.commit()

    def eliminar_tarea(self, tarea_id):  #Borra la tarea y su ID, Nunca se vuelve a reutilizar la misma ID.
        query = '''
        DELETE FROM tareas WHERE id = ?
        '''
        self.cursor.execute(query, (tarea_id,))
        self.conn.commit()

    def traer_todas_tareas(self):   #Revisar
        query = '''
        SELECT * FROM tareas
        '''
        self.cursor.execute(query)
        tareas_data = self.cursor.fetchall()
        tareas = []
        for tarea_data in tareas_data:
            tarea = Tarea(
                tarea_data[1],
                tarea_data[2],
                tarea_data[3],
                datetime.fromisoformat(tarea_data[4]),
                datetime.fromisoformat(tarea_data[5])
            )
            tarea.tarea_id = tarea_data[0]  # Agregar el atributo tarea_id a la tarea
            tareas.append(tarea)
        return tareas

    def agregar_persona(self, persona):
        query = '''
        INSERT INTO personas (nombre, contraseña)
        VALUES (?, ?)
        '''
        contraseña_codificada = hashlib.md5(persona.contraseña.encode()).hexdigest()
        values = (persona.nombre, contraseña_codificada)
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor.lastrowid
    

    def verificar_credenciales(self, nombre, contraseña):    #Se posiciona el cursor en Personas de DataBase y verifica 
        query = '''
        SELECT * FROM personas WHERE nombre = ? AND contraseña = ?
        '''
        contraseña_codificada = hashlib.md5(contraseña.encode()).hexdigest()
        self.cursor.execute(query, (nombre, contraseña_codificada))
        persona_data = self.cursor.fetchone()
        if persona_data:
            return True
        return False

def mostrar_menu():  #MENU TERMINAL, TIENE QUE REMPLAZARSE POR UNO GRAFICO 
    print("=== Menú de Tareas ===")
    print("1. Agregar tarea")
    print("2. Ver tarea")
    print("3. Actualizar estado de tarea")
    print("4. Eliminar tarea")
    print("5. Ver todas las tareas")
    print("0. Salir")

def agregar_tarea(admin):
    titulo = input("Ingrese el título de la tarea: ")
    descripcion = input("Ingrese la descripción de la tarea: ")
    tarea = Tarea(titulo, descripcion)
    tarea_id = admin.agregar_tarea(tarea)
    print(f"Tarea agregada con ID: {tarea_id}")

def ver_tarea(admin):
    tarea_id = int(input("Ingrese el ID de la tarea: "))
    tarea = admin.traer_tarea(tarea_id)
    if tarea:
        print(f"Título: {tarea.titulo}")
        print(f"Descripción: {tarea.descripcion}")
        print(f"Estado: {tarea.estado}")
        print(f"Creada: {tarea.creada}")
        print(f"Actualizada: {tarea.actualizada}")
    else:
        print("No se encontró ninguna tarea con ese ID")

def actualizar_estado(admin):
    tarea_id = int(input("Ingrese el ID de la tarea: "))
    estado = input("Ingrese el nuevo estado de la tarea: ")
    admin.actualizar_estado_tarea(tarea_id, estado)
    print("Estado de la tarea actualizado correctamente")   

def eliminar_tarea(admin):
    tarea_id = int(input("Ingrese el ID de la tarea: "))
    admin.eliminar_tarea(tarea_id)
    print("Tarea eliminada correctamente")

def ver_todas_tareas(admin):
    tareas = admin.traer_todas_tareas()
    if tareas:
        for tarea in tareas:
            print(f"ID: {tarea.tarea_id}, Título: {tarea.titulo}, Descripción: {tarea.descripcion}, Estado: {tarea.estado}")
    else:
        print("No hay tareas registradas")

def verificar_credenciales(admin):
    nombre = input("Ingrese su nombre: ")
    contraseña = input("Ingrese su contraseña: ")
    if admin.verificar_credenciales(nombre, contraseña):
        return True
    else:
        print("Credenciales inválidas. Acceso denegado.")
        return False

# Crear una instancia de AdminTarea con usuario admin  

admin = AdminTarea('database.sqlite')   #Esto crea la base de datos
persona1 = Persona("admin", "admin")   #Esto crea usuario "ADMIN"
admin.agregar_persona(persona1)   #Se va a data base codificando contraseña

app = Flask(__name__)


@app.route("/verificar", methods=['POST'])
def verificar():
    data = request.get_json()
    nombre = data['nombre']
    contraseña = data['contraseña']
    if admin.verificar_credenciales(nombre, contraseña):
        return jsonify({"mensaje": "Credenciales validadas correctamente."}), 200
    else:
        return jsonify({"mensaje": "Credenciales inválidas. Acceso denegado."}), 401

@app.route("/tarea", methods=['POST'])
def agregar_tarea():
    data = request.get_json()
    titulo = data['titulo']
    descripcion = data['descripcion']
    tarea = Tarea(titulo, descripcion)
    tarea_id = admin.agregar_tarea(tarea)
    return jsonify({"mensaje": f"Tarea agregada con ID: {tarea_id}"}), 201

@app.route("/tarea/<int:tarea_id>", methods=['GET'])
def ver_tarea(tarea_id):
    tarea = admin.traer_tarea(tarea_id)
    if tarea:
        return jsonify({
            "titulo": tarea.titulo,
            "descripcion": tarea.descripcion,
            "estado": tarea.estado,
            "creada": tarea.creada.isoformat(),
            "actualizada": tarea.actualizada.isoformat()
        }), 200
    else:
        return jsonify({"mensaje": "No se encontró ninguna tarea con ese ID"}), 404

@app.route("/tarea/<int:tarea_id>", methods=['PUT'])
def actualizar_estado(tarea_id):
    data = request.get_json()
    estado = data['estado']
    admin.actualizar_estado_tarea(tarea_id, estado)
    return jsonify({"mensaje": "Estado de la tarea actualizado correctamente"}), 200  

@app.route("/tarea/<int:tarea_id>", methods=['DELETE'])
def eliminar_tarea(tarea_id):
    admin.eliminar_tarea(tarea_id)
    return jsonify({"mensaje": "Tarea eliminada correctamente"}), 200

@app.route("/tareas", methods=['GET'])
def ver_todas_tareas():
    tareas = admin.traer_todas_tareas()
    if tareas:
        tareas_dict = [
            {
                "id": tarea.tarea_id,
                "titulo": tarea.titulo,
                "descripcion": tarea.descripcion,
                "estado": tarea.estado,
                "creada": tarea.creada.isoformat(),
                "actualizada": tarea.actualizada.isoformat()
            }
            for tarea in tareas
        ]
        return jsonify(tareas_dict), 200
    else:
        return jsonify({"mensaje": "No hay tareas registradas"}), 404

if __name__ == "__main__":
    persona1 = Persona("admin", generate_password_hash("admin"))
    admin.agregar_persona(persona1)
    app.run(debug=True)
