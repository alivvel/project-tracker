import sqlite3
import os

#indica la direccion donde esta la db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "media.db")

def crear_base():
    conexion = sqlite3.connect(DB_PATH)
    conexion.close()

def crear_tabla():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT,
            nombre TEXT,
            genero TEXT,
            estado TEXT,
            estrellas INTEGER,
            resena TEXT
        )
    """)

    conexion.commit()
    conexion.close()


def insertar_registro(categoria, nombre, genero, estado, estrellas, resena):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO media (categoria, nombre, genero, estado, estrellas, resena)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (categoria, nombre, genero, estado, estrellas, resena))
    # los ? ? me indican los paramatros
    conexion.commit()           
    conexion.close()

def todos_los_registros_database():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    #nombro cada columna por que con * me da todo (incluyendo el id que no quiero)
    cursor.execute(""" 
        SELECT categoria, nombre, genero, estado, estrellas, resena FROM media""" ) 

    registros = cursor.fetchall() 
   
    conexion.commit()
    conexion.close()
    
    return registros

def ids_database():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute("""SELECT id FROM media""" ) 

    ids = cursor.fetchall() 
   
    conexion.commit()
    conexion.close()
    
    return ids
 
def borrar_registro_database(id):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute(""" DELETE FROM media WHERE id = ?""", (id,) ) 
   
    conexion.commit()
    conexion.close()

def actualizar_database(estado, calificacion, resena, idd):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    cursor.execute(""" 
        UPDATE media 
        SET estado = ?, estrellas = ?, resena = ? WHERE id = ?""", 
        (estado, calificacion, resena, idd))
    
    conexion.commit()
    conexion.close()    

def filtrar_pendientes_db():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute("""SELECT categoria, nombre, genero FROM media 
                   WHERE estado = 'Pendiente' OR estado = 'En curso'""")
    
    pendientes = cursor.fetchall()
    
    conexion.commit()
    conexion.close()
    return pendientes