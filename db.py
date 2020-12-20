import sqlite3
from sqlite3 import Error

con=None #variable global para conxion

def get_db():
    try:
        con=sqlite3.connect('DB/brioche.db')
        # print('Conexión con DB OK.')
        return con
    except :
        print('Error al conectar DB.')

def close_db():
    if con is not None: 
        con.close()
       