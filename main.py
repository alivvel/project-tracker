import tkinter as tk
from database import *
from ui import * 

crear_base()
crear_tabla()

root = tk.Tk()  
app = App(root)

root.mainloop()

