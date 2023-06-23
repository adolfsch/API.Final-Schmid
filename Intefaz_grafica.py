import tkinter as tk
from tkinter import messagebox
import requests


class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.label_username = tk.Label(self.frame, text="Usuario")
        self.label_username.pack()

        self.entry_username = tk.Entry(self.frame)
        self.entry_username.pack()

        self.label_password = tk.Label(self.frame, text="Contraseña")
        self.label_password.pack()

        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.pack()

        self.button_login = tk.Button(self.frame, text="Iniciar sesión", command=self.login)
        self.button_login.pack()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        response = requests.post('http://localhost:8000/login/', json={'nombre': username, 'contraseña': password})

        if response.status_code == 200:
            self.frame.destroy()
            TasksWindow(self.master)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")


class TasksWindow:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.tasks_list = tk.Listbox(self.frame)
        self.tasks_list.pack()

        self.button_refresh = tk.Button(self.frame, text="Actualizar", command=self.refresh_tasks)
        self.button_refresh.pack()

        self.label_new_task = tk.Label(self.frame, text="Nueva tarea")
        self.label_new_task.pack()

        self.entry_new_task = tk.Entry(self.frame)
        self.entry_new_task.pack()

        self.button_add = tk.Button(self.frame, text="Añadir tarea", command=self.add_task)
        self.button_add.pack()

        self.button_delete = tk.Button(self.frame, text="Eliminar tarea", command=self.delete_task)
        self.button_delete.pack()

        self.refresh_tasks()

    def refresh_tasks(self):
        response = requests.get('http://localhost:8000/tareas/')
        tasks = response.json()

        self.tasks_list.delete(0, tk.END)
        for task in tasks:
            self.tasks_list.insert(tk.END, task['titulo'])

    def add_task(self):
        new_task_title = self.entry_new_task.get()
        if new_task_title:
            requests.post('http://localhost:8000/tareas/', json={
                'titulo': new_task_title,
                'descripcion': 'Descripción',  # Modificar para tomar la descripción de la interfaz gráfica
                'estado': 'pendiente',  # Modificar para tomar el estado de la interfaz gráfica
                'creada': '2023-07-01T10:00:00',  # Modificar para tomar la fecha de creación actual
                'actualizada': '2023-07-01T10:00:00'  # Modificar para tomar la fecha de actualización actual
            })
            self.refresh_tasks()

    def delete_task(self):
        task_title = self.tasks_list.get(self.tasks_list.curselection())
        if task_title:
            # Asumiendo que tienes un endpoint para eliminar tarea por título. Si no lo tienes, necesitarás obtener la tarea por título, obtener su ID y luego eliminarla por ID.
            requests.delete(f'http://localhost:8000/tareas/{task_title}/')
            self.refresh_tasks()


def main():
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
