""" Gestor de Tareas con Interfaz Gráfica

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
        self.root.config(bg="dark green")  # Fondo de la ventana

        self.frame_tareas = tk.Frame(self.root, bg="dark green")  
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
        menu_tareas.add_command(label="Cargar Listado", command=self.cargar_listado)  

        # Agregar el menú a la barra de menú
        menu_bar.add_cascade(label="Opciones", menu=menu_tareas)

        # Configurar la ventana para que use esta barra de menú
        self.root.config(menu=menu_bar)

        self.cargar_listado()  # Carga automática al iniciar

    def agregar_tarea(self, texto="", fecha="", estado=False):
        frame_tarea = tk.Frame(self.frame_tareas, bg="dark green", pady=5, padx=5, relief="ridge", bd=2)
        frame_tarea.pack(fill="x", pady=2)

        entry_tarea = tk.Entry(frame_tarea, bg="black", fg="white", borderwidth=1)  
        entry_tarea.pack(side="left", fill="x", expand=True)
        entry_tarea.insert(0, texto)  
        entry_tarea.focus()

        fecha_creacion = fecha if fecha else datetime.datetime.now().strftime("%d/%m/%Y")
        label_fecha = tk.Label(frame_tarea, text=fecha_creacion, bg="dark green", fg="white", width=12)
        label_fecha.pack(side="left")

        var_estado = tk.BooleanVar(value=estado)
        check_boton = tk.Checkbutton(frame_tarea, variable=var_estado, bg="dark green", fg="white", selectcolor="black")
        check_boton.pack(side="right")

        if estado:
            entry_tarea.config(bg="green", fg="white")

        self.tareas.append({"frame": frame_tarea, "entry": entry_tarea, "label_fecha": label_fecha, "estado": var_estado})

    def eliminar_tareas(self):
        for tarea in self.tareas[:]:
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
                tarea["entry"].config(bg="black", fg="white")
                tarea["estado"].set(False)

    def modificar_tarea(self):
        for tarea in self.tareas:
            if tarea["estado"].get():
                tarea["entry"].config(state="normal")

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

                # Limpiar tareas actuales antes de cargar nuevas
                for tarea in self.tareas:
                    tarea["frame"].destroy()
                self.tareas.clear()

                for tarea in lista_cargada:
                    self.agregar_tarea(tarea["texto"], tarea["fecha"], tarea["estado"])

# Crear ventana principal
root = tk.Tk()
app = GestorTareas(root)
root.mainloop()






