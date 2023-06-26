import sqlite3
from fastapi import FastAPI, HTTPException
from Clases import AdminTarea, Tarea as ClaseTarea, Persona as ClasePersona
from pydantic import BaseModel
import uvicorn

app = FastAPI()
conn = sqlite3.connect('database.sqlite')   #Por las dudas lo dejo
admin_tarea = AdminTarea('database.sqlite')

class Tarea(BaseModel):
    titulo: str
    descripcion: str
    estado: str
    creada: str
    actualizada: str

class Persona(BaseModel):
    nombre: str
    contraseña: str

@app.post("/tareas/")
async def crear_tarea(tarea: Tarea):
    tarea_obj = ClaseTarea(tarea.titulo, tarea.descripcion, tarea.estado, tarea.creada, tarea.actualizada)
    nueva_tarea_id = admin_tarea.agregar_tarea(tarea_obj)
    return {"tarea_id": nueva_tarea_id}

@app.get("/tareas/{tarea_id}")
async def obtener_tarea(tarea_id: int):
    tarea = admin_tarea.traer_tarea(tarea_id)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"id": tarea_id, **vars(tarea)}

@app.put("/tareas/{tarea_id}")
async def actualizar_tarea(tarea_id: int, tarea: Tarea):
    admin_tarea.actualizar_estado_tarea(tarea_id, tarea.estado)
    return {"mensaje": "Tarea actualizada"}

@app.delete("/tareas/{tarea_id}")
async def borrar_tarea(tarea_id: int):
    admin_tarea.eliminar_tarea(tarea_id)
    return {"mensaje": "Tarea eliminada"}

@app.get("/tareas/")
async def obtener_todas_tareas():
    tareas = admin_tarea.traer_todas_tareas()
    return [{"id": i, **vars(tarea)} for i, tarea in enumerate(tareas, start=1)]

@app.post("/personas/")
async def agregar_persona(persona: Persona):
    persona_obj = ClasePersona(persona.nombre, persona.contraseña)
    nueva_persona_id = admin_tarea.agregar_persona(persona_obj)
    return {"persona_id": nueva_persona_id}

@app.post("/login/")
async def login(persona: Persona):
    es_valido = admin_tarea.verificar_credenciales(persona.nombre, persona.contraseña)
    if not es_valido:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {"mensaje": "Inicio de sesión exitoso"}

uvicorn.run(app, host="localhost", port=8000) #En vez de siempre poner uvicorn API:app --reload