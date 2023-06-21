import sqlite3
import hashlib
from datetime import datetime
from flask import Flask, jsonify, request
 
app = Flask(__name__)          ###HACERLO API Con Requests

class Tarea:
    def __init__(self, titulo, descripcion, estado='pendiente', creada=None, actualizada=None):
        self.titulo = titulo
        self.descripcion = descripcion
        self.estado = estado
        self.creada = creada or datetime.now()
        self.actualizada = actualizada or datetime.now()

class Persona:
    def __init__(self, nombre, contrasena):
        self.nombre = nombre
        self.contrasena = contrasena

class AdminTarea:
    def __init__(self, db_path):
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
            contrasena TEXT
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

    def eliminar_tarea(self, tarea_id):
        query = '''
        DELETE FROM tareas WHERE id = ?
        '''
        self.cursor.execute(query, (tarea_id,))
        self.conn.commit()

    def traer_todas_tareas(self):
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
            tarea.tarea_id = tarea_data[0]
            tareas.append(tarea)
        return tareas

    def agregar_persona(self, persona):
        query = '''
        INSERT INTO personas (nombre, contrasena)
        VALUES (?, ?)
        '''
        contrasena_codificada = hashlib.md5(persona.contrasena.encode()).hexdigest()
        values = (persona.nombre, contrasena_codificada)
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor.lastrowid

    def verificar_credenciales(self, nombre, contrasena):
        query = '''
        SELECT * FROM personas WHERE nombre = ? AND contrasena = ?
        '''
        contrasena_codificada = hashlib.md5(contrasena.encode()).hexdigest()
        self.cursor.execute(query, (nombre, contrasena_codificada))
        persona_data = self.cursor.fetchone()
        if persona_data:
            return True
        return False

# Crear una instancia de AdminTarea con usuario admin
admin = AdminTarea('db.sqlite')
persona1 = Persona("admin", "admin")
admin.agregar_persona(persona1)

# Rutas de la API
@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    tareas = admin.traer_todas_tareas()
    tareas_json = []
    for tarea in tareas:
        tarea_json = {
            'id': tarea.tarea_id,
            'titulo': tarea.titulo,
            'descripcion': tarea.descripcion,
            'estado': tarea.estado,
            'creada': tarea.creada.isoformat(),
            'actualizada': tarea.actualizada.isoformat()
        }
        tareas_json.append(tarea_json)
    return jsonify(tareas_json)

@app.route('/tareas', methods=['POST'])
def agregar_tarea():
    data = request.get_json()
    titulo = data['titulo']
    descripcion = data['descripcion']
    tarea = Tarea(titulo, descripcion)
    tarea_id = admin.agregar_tarea(tarea)
    return jsonify({'id': tarea_id}), 201

@app.route('/tareas/<int:tarea_id>', methods=['GET'])
def obtener_tarea(tarea_id):
    tarea = admin.traer_tarea(tarea_id)
    if tarea:
        tarea_json = {
            'id': tarea.tarea_id,
            'titulo': tarea.titulo,
            'descripcion': tarea.descripcion,
            'estado': tarea.estado,
            'creada': tarea.creada.isoformat(),
            'actualizada': tarea.actualizada.isoformat()
        }
        return jsonify(tarea_json)
    return jsonify({'mensaje': 'Tarea no encontrada'}), 404

@app.route('/tareas/<int:tarea_id>', methods=['PUT'])
def actualizar_estado_tarea(tarea_id):
    data = request.get_json()
    estado = data['estado']
    admin.actualizar_estado_tarea(tarea_id, estado)
    return jsonify({'mensaje': 'Estado de tarea actualizado correctamente'})

@app.route('/tareas/<int:tarea_id>', methods=['DELETE'])
def eliminar_tarea(tarea_id):
    admin.eliminar_tarea(tarea_id)
    return jsonify({'mensaje': 'Tarea eliminada correctamente'})

if __name__ == '__main__':
    app.run()
