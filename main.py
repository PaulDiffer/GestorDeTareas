""" Gestor de Tareas con Interfaz Gráfica
1-Usar Tkinter o PyQt para la interfaz.
2-Permite agregar, eliminar y marcar tareas como completadas.
3-Guarda las tareas en un archivo JSON o SQLite.
¿Qué hace este código?
✔ Muestra una ventana con una barra de menú.
✔ Al presionar "Agregar tarea", se muestra un cuadro de diálogo para ingresar texto.
✔ La tarea se muestra con fondo blanco, texto negro y fecha de creación.
✔ Un Checkbutton permite marcar o desmarcar la tarea.
✔ "Marcar tarea como completada" cambia el fondo a verde con texto blanco.
✔ "Eliminar tarea" borra las tareas marcadas.
"""


import tkinter as tk
import datetime
import json
import os

class GestorTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        
        self.frame_tareas = tk.Frame(self.root)
        self.frame_tareas.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.tareas = []

        # Crear barra de menú
        menu_bar = tk.Menu(self.root)
        menu_tareas = tk.Menu(menu_bar, tearoff=0)
        menu_tareas.add_command(label="Agregar tarea", command=self.agregar_tarea)
        menu_tareas.add_command(label="Borrar tareas seleccionadas", command=self.eliminar_tareas)
        menu_tareas.add_command(label="Marcar tarea como completada", command=self.marcar_completadas)
        menu_tareas.add_command(label="Desmarcar tarea como realizada", command=self.desmarcar_completadas)
        menu_tareas.add_command(label="Modificar tarea", command=self.modificar_tarea)
        menu_tareas.add_command(label="Guardar Listado", command=self.guardar_listado)
        
        menu_bar.add_cascade(label="Tareas", menu=menu_tareas)
        self.root.config(menu=menu_bar)

        self.cargar_listado()  # Cargar tareas guardadas

    def agregar_tarea(self, texto="", fecha="", estado=False):
        # Crear un contenedor para la tarea
        frame_tarea = tk.Frame(self.frame_tareas, bg="white", pady=5, padx=5, relief="ridge", bd=2)
        frame_tarea.pack(fill="x", pady=2)

        # Entrada de texto para la tarea
        entry_tarea = tk.Entry(frame_tarea, bg="white", fg="black", borderwidth=1)
        entry_tarea.pack(side="left", fill="x", expand=True)
        entry_tarea.insert(0, texto)  # Si se cargan desde JSON
        entry_tarea.focus()  # Para que el cursor aparezca directamente

        # Mostrar la fecha de creación
        fecha_creacion = fecha if fecha else datetime.datetime.now().strftime("%d/%m/%Y")
        label_fecha = tk.Label(frame_tarea, text=fecha_creacion, bg="white", fg="black", width=12)
        label_fecha.pack(side="left")

        # Checkbox para marcar la tarea
        var_estado = tk.BooleanVar(value=estado)
        check_boton = tk.Checkbutton(frame_tarea, variable=var_estado)
        check_boton.pack(side="right")

        if estado:
            entry_tarea.config(bg="green", fg="white")

        self.tareas.append({"frame": frame_tarea, "entry": entry_tarea, "label_fecha": label_fecha, "estado": var_estado})

    def eliminar_tareas(self):
        for tarea in self.tareas[:]:  # Copia de la lista para evitar problemas al eliminar elementos
            if tarea["estado"].get():
                tarea["frame"].destroy()
                self.tareas.remove(tarea)

    def marcar_completadas(self):
        for tarea in self.tareas:
            if tarea["estado"].get():
                tarea["entry"].config(bg="green", fg="white")

    def desmarcar_completadas(self):
        for tarea in self.tareas:
            if tarea["estado"].get():
                tarea["entry"].config(bg="white", fg="black")
                tarea["estado"].set(False)  # Desmarca el checkbox

    def modificar_tarea(self):
        for tarea in self.tareas:
            if tarea["estado"].get():
                tarea["entry"].config(state="normal")  # Permite editar nuevamente

    def guardar_listado(self):
        lista_guardada = []
        for tarea in self.tareas:
            lista_guardada.append({
                "texto": tarea["entry"].get(),
                "fecha": tarea["label_fecha"].cget("text"),
                "estado": tarea["estado"].get()
            })
        
        with open("tareas.json", "w", encoding="utf-8") as archivo:
            json.dump(lista_guardada, archivo, indent=4)

    def cargar_listado(self):
        if os.path.exists("tareas.json"):
            with open("tareas.json", "r", encoding="utf-8") as archivo:
                lista_cargada = json.load(archivo)
                for tarea in lista_cargada:
                    self.agregar_tarea(tarea["texto"], tarea["fecha"], tarea["estado"])

# Crear ventana principal
root = tk.Tk()
app = GestorTareas(root)
root.mainloop()
