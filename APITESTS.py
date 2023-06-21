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

class Persona:    #ESTA CLASE VA A ALMACENAR LA PERSONA DENTRO DE LA DATABASE
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
            tarea.tarea_id = tarea_data[0]  # Agregar el atributo tarea_id a la tarea
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
    contrasena = input("Ingrese su contraseña: ")
    if admin.verificar_credenciales(nombre, contrasena):
        return True
    else:
        print("Credenciales inválidas. Acceso denegado.")
        return False

# Crear una instancia de AdminTarea con usuario admin  

admin = AdminTarea('db.sqlite')   #Esto crea la base de datos
persona1 = Persona("admin", "admin")   #Esto crea usuario "ADMIN"
admin.agregar_persona(persona1)

# Verificar credenciales
if verificar_credenciales(admin):
    # Menú principal
    while True:
        mostrar_menu()
        opcion = input("Ingrese una opción: ")
        
        if opcion == '1':
            agregar_tarea(admin)
        elif opcion == '2':
            ver_tarea(admin)
        elif opcion == '3':
            actualizar_estado(admin)
        elif opcion == '4':
            eliminar_tarea(admin)
        elif opcion == '5':
            ver_todas_tareas(admin)
        elif opcion == '0':
            print("Saliendo del programa. Vuelva pronto!")
            break
        else:
            print("Opción inválida. Por favor, ingresa una opción válida.")
else:
    print("Acceso denegado. Verifique sus credenciales.")

