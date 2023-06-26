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
        contraseña_codificada = hashlib.md5(contraseña.encode()).hexdigest()  #agarra la contraseña de terminal, hashea y verifica
        self.cursor.execute(query, (nombre, contraseña_codificada))                 
        persona_data = self.cursor.fetchone()
        if persona_data:
            return True
        return False
    


# Crear una instancia de AdminTarea con usuario admin  

admin = AdminTarea('database.sqlite')   #Esto crea la base de datos
persona1 = Persona("admin", "admin")   #Esto crea usuario "ADMIN"
admin.agregar_persona(persona1)   #Se va a data base codificando contraseña

#conn = sqlite3.connect('database.sqlite')
#cursor = conn.cursor()
#conn.commit()
#conn.close()