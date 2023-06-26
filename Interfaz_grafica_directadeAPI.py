import requests
import tkinter as tk
from tkinter import messagebox, simpledialog

#& C:/Users/adolf/AppData/Local/Programs/Python/Python311/python.exe "c:/Users/adolf/Desktop/testeos Practico Final/Interfaz_grafica_directadeAPI.py"


# Crear la ventana de inicio de sesión
root = tk.Tk()      
root.geometry('300x200')

nombre_entry = tk.StringVar()   #es una clase en tkinter para manejar variables de cadena de texto, no funcaba el request de abajo
contraseña_entry = tk.StringVar()

def verificar_credenciales():
    nombre = nombre_entry.get()
    contraseña = contraseña_entry.get()
    response = requests.post('http://localhost:8000/login/', json={"nombre": nombre, "contraseña": contraseña})
    if response.status_code == 200:
        messagebox.showinfo(message="Inicio de sesión perfecto", title="Login")
        root.destroy()   #Esconde la ventana
        mostrar_tareas()
    else:
        messagebox.showinfo(message="Credenciales inválidas, llamando a policia...", title="Login")


username_label = tk.Label(root, text='Nombre')
username_entry = tk.Entry(root, textvariable=nombre_entry)
password_label = tk.Label(root, text='Contraseña')
password_entry = tk.Entry(root, textvariable=contraseña_entry, show='*')
login_button = tk.Button(root, text='Iniciar sesión', command=verificar_credenciales)

username_label.pack()
username_entry.pack()
password_label.pack()
password_entry.pack()
login_button.pack()

def mostrar_tareas():
    tareas_window = tk.Tk()    # Creamos una nueva ventana para mostrar las tareas
    tareas_window.geometry('800x600')

    tareas_frame = tk.Frame(tareas_window)
    tareas_frame.pack(side=tk.TOP)

    botones_frame = tk.Frame(tareas_window)
    botones_frame.pack(side=tk.BOTTOM)

    def refrescar_tareas():
        for widget in tareas_frame.winfo_children():
            widget.destroy()

        response = requests.get('http://localhost:8000/tareas/')

        if response.status_code == 200:
            tareas = response.json()
            for tarea in tareas:
                label = tk.Label(tareas_frame, text=f'ID: {tarea["id"]} {tarea["titulo"]} - {tarea["descripcion"]} \n Creada: {tarea["creada"]} \n Actualizada: {tarea["actualizada"]}')
                label.pack()

    def agregar_tarea():
        tarea_titulo = simpledialog.askstring("Input", "¿Cuál es el título de la tarea?")
        tarea_descripcion = simpledialog.askstring("Input", "¿Cuál es la descripción de la tarea?")
        tarea_estado = simpledialog.askstring("Input", "¿Cuál es el estado de la tarea?")
    
        response = requests.post('http://localhost:8000/tareas/', json={"titulo": tarea_titulo, "descripcion": tarea_descripcion, "estado": tarea_estado, "creada": "", "actualizada": ""})

        if response.status_code == 200:
            messagebox.showinfo(message="Tarea creada con éxito", title="Tareas")
            refrescar_tareas()
        else:
            messagebox.showinfo(message="Error al crear la tarea", title="Tareas")

    def actualizar_tarea():
        tarea_id = simpledialog.askstring("Input", "¿Cuál es el ID de la tarea que quieres actualizar?")
        tarea_estado = simpledialog.askstring("Input", "¿Cuál es el nuevo estado de la tarea?")
    
        response = requests.put(f'http://localhost:8000/tareas/{tarea_id}', json={"estado": tarea_estado, "titulo": "", "descripcion": "", "creada": "", "actualizada": ""})

        if response.status_code == 200:
            messagebox.showinfo(message="Tarea actualizada con éxito", title="Tareas")
            refrescar_tareas()
        else:
            messagebox.showinfo(message="Error al actualizar la tarea", title="Tareas")

    def eliminar_tarea():
        tarea_id = simpledialog.askstring("Input", "¿Cuál es el ID de la tarea que quieres eliminar?")
    
        response = requests.delete(f'http://localhost:8000/tareas/{tarea_id}')

        if response.status_code == 200:
            messagebox.showinfo(message="Tarea eliminada con éxito", title="Tareas")
            refrescar_tareas()
        else:
            messagebox.showinfo(message="Error al eliminar la tarea", title="Tareas")

    boton_agregar = tk.Button(botones_frame, text='Agregar tarea', command=agregar_tarea)
    boton_actualizar = tk.Button(botones_frame, text='Actualizar tarea', command=actualizar_tarea)
    boton_eliminar = tk.Button(botones_frame, text='Eliminar tarea', command=eliminar_tarea)
    boton_refrescar = tk.Button(botones_frame, text='Refrescar tareas', command=refrescar_tareas)

    boton_agregar.pack()
    boton_actualizar.pack()
    boton_eliminar.pack()
    boton_refrescar.pack()
    refrescar_tareas() #Lo dejo por si se traban en las demas funciones
