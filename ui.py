import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import *

#una clase una ventana
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("TRACKER")
        self.root.configure(bg = '#FDB3FF')
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        
        boton_que_veo_ahora = tk.Button(self.root, text = "¿Que veo ahora?", command=self.abrir_ventana_queVeoAhora, fg = "white", bg = "red")
        boton_que_veo_ahora.grid(row= 0, column= 2, padx=10, pady=10)
        
        self.crear_formulario()
        self.crear_treeview()
    
    def crear_formulario(self):
        
        label_style = {"bg" : "#FFD1FF", "fg" : "#F01CF7"} 
        entry_style = {"bg" : "#F5F2F5", "fg" : "#F321FA"}


        form_frame = tk.Frame(self.root, bg="#FFD1FF", bd=2, relief="groove")
        form_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)
        form_frame.grid_columnconfigure(2, weight=1)

        #0 
        label_categoria = tk.Label(form_frame, text = "Categoria" , **label_style) 
        label_categoria.grid(row=0, column=0, padx=10, pady=5)

        #uso self aca asi puedo acceder a ellas desde otras funciones (las hace globales dentro de la clase)
        self.combo_categoria = ttk.Combobox(
            form_frame,                     
            values=["Película", "Serie", "Libro", "Manga"],
            state="readonly"              # evita que escriban texto libre
        )
        self.combo_categoria.grid(row=0, column=1, padx=10, pady=5)
    
        #1
        label_nombre = tk.Label(form_frame, text = "Nombre" , **label_style) 
        label_nombre.grid(row=1, column=0, padx=10, pady=5) 
        self.entry_nombre = tk.Entry(form_frame, **entry_style)
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=5)
        #2
        label_genero = tk.Label(form_frame, text = "Genero" , **label_style) 
        label_genero.grid(row=2, column=0, padx=10, pady=5) 
        
        self.combo_genero = ttk.Combobox(
            form_frame,                     
            values=["Romance", "Fantasia", "Drama", "Bl", "Ciencia Ficcion", "Thriller"],
            state="readonly"           
        )
        self.combo_genero.grid(row=2, column=1, padx=10, pady=5)
        #3
        label_estado = tk.Label(form_frame, text = "Estado" , **label_style) 
        label_estado.grid(row=3, column=0, padx=10, pady=5) 
        
        self.combo_estado = ttk.Combobox(
            form_frame,                     
            values=["Pendiente", "En curso", "Terminada"],
            state="readonly"           
        )
        self.combo_estado.grid(row=3, column=1, padx=10, pady=5)
        
        #4
        label_calificacion = tk.Label(form_frame, text = "Calificacion" , **label_style) 
        label_calificacion.grid(row=4, column=0, padx=10, pady=5) 
        self.entry_calificacion = tk.Entry(form_frame, **entry_style)
        self.entry_calificacion.grid(row=4, column=1, padx=10, pady=5)
        #5
        label_resena = tk.Label(form_frame, text = "Reseña" , **label_style) 
        label_resena.grid(row=5, column=0, padx=10, pady=5) 
        self.entry_resena = tk.Entry(form_frame, **entry_style)
        self.entry_resena.grid(row=5, column=1, padx=10, pady=5)

        #creo que el boton
        boton_guardar = tk.Button(form_frame, text = "GUARDAR", command=self.guardar_registro, fg =  "#F9F9F9", bg = "#E931EF" )
        boton_guardar.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
           
    def guardar_registro(self):
        #guardo las variables
        categoria = self.combo_categoria.get()
        nombre = self.entry_nombre.get()
        genero = self.combo_genero.get()
        estado = self.combo_estado.get()
        calificacion = self.entry_calificacion.get()
        resena = self.entry_resena.get()

        if not categoria or not nombre or not genero or not estado:
            messagebox.showwarning("Error", "Completá los campos obligatorios")
            return
        if calificacion:
            try:
                calificacion = int(calificacion)
            except ValueError:
                messagebox.showerror("Error", "La calificación debe ser un número")
            
        #llamo a funcion del database
        insertar_registro(categoria, nombre, genero, estado, calificacion, resena)
        #busco el nuevo id de la db
        id_db=ids_database()
        id_nuevo= id_db[len(id_db)-1]
        #guardo el registro nuevo en el treeview
        self.tree.insert("", tk.END, iid=id_nuevo, values=(categoria, nombre, genero, estado, calificacion, resena))
    
        messagebox.showinfo("Éxito", "Registro guardado correctamente")

        # Limpiar campos
        self.combo_categoria.set("")
        self.entry_nombre.delete(0, tk.END)
        self.combo_genero.set("")
        self.combo_estado.set("")
        self.entry_calificacion.delete(0, tk.END)
        self.entry_resena.delete(0, tk.END)
    
    def crear_treeview(self):
        #creo un treeView con frame
        frame_tree = tk.Frame(self.root)
        frame_tree.configure(bg = '#FDB3FF')
        frame_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        frame_tree.grid_rowconfigure(0, weight=1)
        frame_tree.grid_columnconfigure(0, weight=1)
        frame_tree.grid_columnconfigure(1, weight=1)
        frame_tree.grid_columnconfigure(2, weight=1)
        frame_tree.grid_columnconfigure(3, weight=1)
        
        self.tree = ttk.Treeview(frame_tree, columns=("Categoria", "Nombre", "Genero", "Estado", "Calificacion", "Reseña"), show= "headings")
        self.tree.grid(row=0, column=0, columnspan=3, sticky="nsew")

        colums = ["Categoria", "Nombre", "Genero", "Estado", "Calificacion", "Reseña"]
        for c in colums:
            self.tree.heading(c, text=c) #escribo el texto en cada identificador
            self.tree.column(c, width=100, anchor="center")
        
        #obtengo los registros de la db  
        registros_db = todos_los_registros_database()
        ids_db = ids_database()
        #los guardo en el treeview
        for idd, registro in zip(ids_db, registros_db): #zip me gusta dos listas
            self.tree.insert("", tk.END, iid=idd, values=registro)
        
        boton_eliminar = tk.Button(frame_tree, text = "ELIMINAR REGISTRO", command=self.eliminar_registro, fg =  "#FFFFFF", bg = "#E931EF" )
        boton_eliminar.grid(row=2, column=1, pady=10)

        boton_actualizar = tk.Button(frame_tree, text = "ACTUALIZAR", command=self.actualizarSeguimiento, fg =  "#FFFFFF", bg = "#E931EF" )
        boton_actualizar.grid(row = 2, column=2, pady=10)
    
    def eliminar_registro(self):
        registro_seleccionado = self.tree.selection() #me da solo el idd pero en tupla : ('3',)
        id = registro_seleccionado[0]
        if messagebox.askyesno("Confirmar", "¿desea eliminar este registro?"):
            self.tree.delete(registro_seleccionado)
            borrar_registro_database(id) #lo elimino de la base de datos
            
    def actualizarSeguimiento(self):
        #codicion para que no me abra otra ventana mientras exista una
        if hasattr(self, "ventana_actualizar") and self.ventana_actualizar.ventana.winfo_exists():
            self.ventana_actualizar.ventana.lift()
            return
        #si no exiate ventana abierta entonces ahora si abro una ventana nueva
        ##guardo el objeto porque py lo elimina automaticamente objetos sin referencia
        self.ventana_actualizar = VentanaActualizar(self)
  
    def abrir_ventana_queVeoAhora(self):
        lista_filtrada = filtrar_pendientes_db()
        self.ventana_filtros = VentanaQueVeoAhora(self, lista_filtrada)
        
        
class VentanaActualizar:
    def __init__(self, master_app):
        self.master_app = master_app #tengo acceso a todo lo de App usando master_app(que es el self de App)
        self.ventana = tk.Toplevel(master_app.root)
        self.ventana.title("Actualiza el seguimiento")
        self.ventana.configure(bg = '#FDB3FF')
        
        self.formulario_actualizar()
        
        #no puedo tocar la ventana principal hasta cerrar la secuntaria
        self.ventana.transient(master_app.root)  # depende de la principal
        self.ventana.grab_set()                  # bloquea interacción con la principal

    def formulario_actualizar(self):
        #valido
        registro_selecc = self.master_app.tree.selection()
        #busco el id del registro seleccionado en el treeview
        self.idd = registro_selecc[0]
        self.list_valores= self.master_app.tree.item(self.idd)["values"]
 
        if not registro_selecc:
            messagebox.showwarning("Error", "Seleccione un registro a actualizar")
            return
        #tambien valido que no quiera actualizar una pelicula que ya termino
        if self.list_valores[3] == "Terminada" :
            messagebox.showinfo("Aviso", "Ya termino y califico esta " + self.list_valores[0].lower())
            return
        
        #creo ventana
        label_style = {"bg" : "#FDB3FF", "fg" : "#F01CF7"} 
        entry_style = {"bg" : "#FDB3FF", "fg" : "#F321FA"}
        labels = ["Categoria", "Nombre", "Genero", "Estado", "Calificacion", "Resena"]
        
        for indice, label in enumerate(labels, start=0):
            tk.Label(self.ventana, text=label, **label_style).grid(row=str(indice), column=0, padx=10, pady=5)
        
        #creo una sub lista para los entry que no tengo que modificar       
        entrys_bloqueados = [self.list_valores[0], self.list_valores[1], self.list_valores[2]]
        
        for i, text_entry in enumerate(entrys_bloqueados, start=0):
            entry_bloq = tk.Entry(self.ventana, **entry_style)
            entry_bloq.insert(0, str(text_entry))
            entry_bloq.config(state="readonly")
            entry_bloq.grid(row=str(i), column=1, padx=10, pady=5)
        
        #ahora si actualzo
        self.combo_estado = ttk.Combobox(
            self.ventana,                     
            values=["Pendiente", "En curso", "Terminada"],
            state="readonly"           
        )
        self.combo_estado.grid(row=3, column=1, padx=10, pady=5)
        
        self.entry_calif = tk.Entry(self.ventana, **entry_style)
        self.entry_calif.grid(row=4, column=1, padx=10, pady=5)    
        
        self. entry_resena = tk.Entry(self.ventana, **entry_style)
        self.entry_resena.grid(row=5, column=1, padx=10, pady=5)
        
        boton_actualizar = tk.Button(self.ventana, text="Actualizar", command=self.guardar_actualizacion, fg =  "#F9F9F9", bg = "#E931EF")
        boton_actualizar.grid(row = 6, column=0, columnspan=2, padx=10, pady=5 )
        
    def guardar_actualizacion(self):
        #valido que no tengo esta misma ventana abierta
        
        estado = self.combo_estado.get()
        calificacion = self.entry_calif.get()
        resena = self.entry_resena.get()
        
        if estado == "Terminada" and not calificacion:
            messagebox.showinfo("Aviso", "Si termino la "+self.list_valores[0]+" califiquela" )
            return
        #modifico mi lista
        self.list_valores[3] = estado
        self.list_valores[4] = calificacion
        self.list_valores[5] = resena
        print("el id: " + self.idd)
        #actualizo el treeview
        self.master_app.tree.item(self.idd, values = self.list_valores)
        actualizar_database(estado, calificacion, resena, self.idd)
        
        
        self.ventana.destroy()
    
class VentanaQueVeoAhora:
    def __init__(self, master_app, lista_filtrada):
        self.master_app = master_app
        self.lista_filtrada = lista_filtrada
        
        self.top = tk.Toplevel(master_app.root)
        self.top.title("¿Que veo ahora?")
        self.top.configure(bg = "#FFD1FF")       
        
        self.vista_filtros()
        self.vista_tree()
        
        self.top.transient(master_app.root)
        self.top.grab_set()
    
    def vista_tree(self):
        tree_frame = tk.Frame(self.top)
        tree_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="w")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(1, weight=1)

        colums = ["Categoria", "Nombre", "Genero"]
        self.mini_tree = ttk.Treeview(tree_frame, columns=colums, show= "headings" )
        self.mini_tree.grid(row=0, column=0, columnspan=4, sticky="nsew")
        
        for c in colums:
            self.mini_tree.heading(c, text=c) 
            self.mini_tree.column(c, width=100, anchor="center")
        
        #como es un treeview de solo vista no necesito poner ids
        for fila in self.lista_filtrada:
            self.mini_tree.insert("", tk.END,values=fila)      
            
    def vista_filtros(self):
        label_style = { "bg" : "#FFD1FF", "fg" : "#F01CF7"} 
        
        #frame de filtros combox
        frame_filtros = tk.Frame(self.top, bg="#FFD1FF")
        frame_filtros.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")
        
        tk.Label(frame_filtros, text="Tenes todas estas peliculas, serie y libros pendientes", **label_style).grid(row=0, column=0, columnspan=3, padx=10, pady=5)
        tk.Label(frame_filtros, text="Categoria", **label_style).grid(row=1, column=0, padx=10, pady=5)
        tk.Label(frame_filtros, text = "Genero" , **label_style).grid(row=2, column=0, padx=10, pady=5) 
        
        self.filtro_categoria = ttk.Combobox(
            frame_filtros,                     
            values=["Película", "Serie", "Libro", "Manga"],
            state="readonly"           
        )
        self.filtro_categoria.grid(row=1, column=1, padx=10, pady=5)
        
        self.filtro_genero = ttk.Combobox(
            frame_filtros,                     
            values=["Romance", "Fantasia", "Drama", "Bl", "Ciencia Ficcion", "Thriller"],
            state="readonly"           
        )
        self.filtro_genero.grid(row=2, column=1, padx=10, pady=5)
        
        boton_filtrar = tk.Button(frame_filtros, text="filtrar", command=self.filtrar_por_genero, fg = "white", bg = "red")
        boton_filtrar.grid(row=1, column=2, padx=10, pady=10)      
        boton_limpiar = tk.Button(frame_filtros, text="Limpiar", command=self.limpiar_filtro, fg = "white", bg = "red")
        boton_limpiar.grid(row=2, column=2, padx=10, pady=10)      
    
    def filtrar_por_genero(self):
        categoria_a_filtrar= self.filtro_categoria.get()
        genero_a_filtrar= self.filtro_genero.get()
        #valido
        if not genero_a_filtrar and not categoria_a_filtrar:
            messagebox.showwarning("Error", "Seleccione una categoria o genero a filtrar")
            return
        
        #hago en el filtro directamente la liosta que me pasaron sin consultar a la db
        lista_sub_filtrada = []
        
        if categoria_a_filtrar and not genero_a_filtrar: #filtro solo x categoria
            for registro in self.lista_filtrada:
                categoria = registro[0]
                if categoria == categoria_a_filtrar:
                    lista_sub_filtrada.append(registro)
                    
        elif genero_a_filtrar and not categoria_a_filtrar: #solo filtro x genero
            for registro in self.lista_filtrada:
                genero = registro[2]
                if genero == genero_a_filtrar:     
                    lista_sub_filtrada.append(registro)
                    
        else: #filtro x categoria y genero
            for registro in self.lista_filtrada:
                if registro[0] == categoria_a_filtrar and registro[2] == genero_a_filtrar:
                    lista_sub_filtrada.append(registro)
                    
        #cuando ya tengo la lista sub filtrada, actualizo el tree view    
        #ahora vacio el mini tree view
        for fila in self.mini_tree.get_children():
            self.mini_tree.delete(fila)

        #agrego la nueva lista filtrada
        for fila in lista_sub_filtrada:
            self.mini_tree.insert("", tk.END,values=fila)      
            
    def limpiar_filtro(self):
        #cuando ya tengo la lista sub filtrada, actualizo el tree view    
        #ahora vacio el mini tree view
        for fila in self.mini_tree.get_children():
            self.mini_tree.delete(fila)

        #agrego la nueva lista filtrada
        for fila in self.lista_filtrada:
            self.mini_tree.insert("", tk.END,values=fila)      
                
    
            