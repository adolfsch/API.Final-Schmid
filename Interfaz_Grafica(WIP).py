import tkinter as tk
from APITESTS import AdminTarea, Tarea

class TaskManagerGUI:
    def __init__(self, admin):
        self.admin = admin

        self.window = tk.Tk()
        self.window.title("Administrador de Tareas")

        self.title_label = tk.Label(self.window, text="Administrador de Tareas")
        self.title_label.pack()

        self.menu_frame = tk.Frame(self.window)
        self.menu_frame.pack()

        self.menu_label = tk.Label(self.menu_frame, text="Menú de Tareas")
        self.menu_label.pack()

        self.add_button = tk.Button(self.menu_frame, text="Agregar Tarea", command=self.agregar_tarea)
        self.add_button.pack()

        self.view_button = tk.Button(self.menu_frame, text="Ver Tarea", command=self.ver_tarea)
        self.view_button.pack()

        self.update_button = tk.Button(self.menu_frame, text="Actualizar Estado", command=self.actualizar_estado)
        self.update_button.pack()

        self.delete_button = tk.Button(self.menu_frame, text="Eliminar Tarea", command=self.eliminar_tarea)
        self.delete_button.pack()

        self.view_all_button = tk.Button(self.menu_frame, text="Ver Todas las Tareas", command=self.ver_todas_tareas)
        self.view_all_button.pack()

    def run(self):
        self.window.mainloop()

    def agregar_tarea(self):
        self.window.withdraw()
        add_window = tk.Toplevel()
        add_window.title("Agregar Tarea")

        title_label = tk.Label(add_window, text="Título:")
        title_label.pack()
        title_entry = tk.Entry(add_window)
        title_entry.pack()

        description_label = tk.Label(add_window, text="Descripción:")
        description_label.pack()
        description_entry = tk.Entry(add_window)
        description_entry.pack()

        def add_task():
            titulo = title_entry.get()
            descripcion = description_entry.get()
            tarea = Tarea(titulo, descripcion)
            tarea_id = self.admin.agregar_tarea(tarea)
            result_label.config(text=f"Tarea agregada con ID: {tarea_id}")

        add_button = tk.Button(add_window, text="Agregar", command=add_task)
        add_button.pack()

        result_label = tk.Label(add_window, text="")
        result_label.pack()

        add_window.protocol("WM_DELETE_WINDOW", self.window.deiconify)
        add_window.mainloop()

    def ver_tarea(self):
        self.window.withdraw()
        view_window = tk.Toplevel()
        view_window.title("Ver Tarea")

        task_id_label = tk.Label(view_window, text="ID de Tarea:")
        task_id_label.pack()
        task_id_entry = tk.Entry(view_window)
        task_id_entry.pack()

        result_label = tk.Label(view_window, text="")

        def view_task():
            tarea_id = int(task_id_entry.get())
            tarea = self.admin.traer_tarea(tarea_id)
            if tarea:
                result_label.config(text=f"Tarea encontrada:\nTítulo: {tarea.titulo}\nDescripción: {tarea.descripcion}\nEstado: {tarea.estado}")
            else:
                result_label.config(text=f"No se encontró una tarea con ID: {tarea_id}")

        view_button = tk.Button(view_window, text="Ver", command=view_task)
        view_button.pack()

        result_label.pack()

        view_window.protocol("WM_DELETE_WINDOW", self.window.deiconify)
        view_window.mainloop()

    def actualizar_estado(self):
        self.window.withdraw()
        update_window = tk.Toplevel()
        update_window.title("Actualizar Estado")

        task_id_label = tk.Label(update_window, text="ID de Tarea:")
        task_id_label.pack()
        task_id_entry = tk.Entry(update_window)
        task_id_entry.pack()

        status_label = tk.Label(update_window, text="Estado:")
        status_label.pack()
        status_entry = tk.Entry(update_window)
        status_entry.pack()

        result_label = tk.Label(update_window, text="")

        def update_task():
            tarea_id = int(task_id_entry.get())
            estado = status_entry.get()
            tarea = self.admin.traer_tarea(tarea_id)
            if tarea:
                self.admin.actualizar_estado_tarea(tarea_id, estado)
                result_label.config(text=f"Estado de la tarea actualizado: {estado}")
            else:
                result_label.config(text=f"No se encontró una tarea con ID: {tarea_id}")

        update_button = tk.Button(update_window, text="Actualizar", command=update_task)
        update_button.pack()

        result_label.pack()

        update_window.protocol("WM_DELETE_WINDOW", self.window.deiconify)
        update_window.mainloop()

    def eliminar_tarea(self):
        self.window.withdraw()
        delete_window = tk.Toplevel()
        delete_window.title("Eliminar Tarea")

        task_id_label = tk.Label(delete_window, text="ID de Tarea:")
        task_id_label.pack()
        task_id_entry = tk.Entry(delete_window)
        task_id_entry.pack()

        result_label = tk.Label(delete_window, text="")

        def delete_task():
            tarea_id = int(task_id_entry.get())
            tarea = self.admin.traer_tarea(tarea_id)
            if tarea:
                self.admin.eliminar_tarea(tarea_id)
                result_label.config(text=f"Tarea eliminada con ID: {tarea_id}")
            else:
                result_label.config(text=f"No se encontró una tarea con ID: {tarea_id}")

        delete_button = tk.Button(delete_window, text="Eliminar", command=delete_task)
        delete_button.pack()

        result_label.pack()

        delete_window.protocol("WM_DELETE_WINDOW", self.window.deiconify)
        delete_window.mainloop()

    def ver_todas_tareas(self):
        self.window.withdraw()
        all_tasks_window = tk.Toplevel()
        all_tasks_window.title("Todas las Tareas")

        tasks = self.admin.traer_todas_tareas()

        if not tasks:
            result_label = tk.Label(all_tasks_window, text="No hay tareas registradas.")
            result_label.pack()
        else:
            for task in tasks:
                task_frame = tk.Frame(all_tasks_window)
                task_frame.pack()

                task_title_label = tk.Label(task_frame, text=f"Título: {task.titulo}")
                task_title_label.pack()

                task_description_label = tk.Label(task_frame, text=f"Descripción: {task.descripcion}")
                task_description_label.pack()

                task_status_label = tk.Label(task_frame, text=f"Estado: {task.estado}")
                task_status_label.pack()

        all_tasks_window.protocol("WM_DELETE_WINDOW", self.window.deiconify)
        all_tasks_window.mainloop()

# Crear una instancia de AdminTarea
admin = AdminTarea('tareas.db')

# Crear una instancia de TaskManagerGUI y ejecutar la aplicación
app = TaskManagerGUI(admin)
app.run()
