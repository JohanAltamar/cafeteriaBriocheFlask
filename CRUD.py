import db
def register(usuario,clave,email):
    print('creando')
    error = None
    #-------------------
    conexion = db.get_db()
    #-------------------
    cur=conexion.cursor()
    print('cursor creado')
    cur.executescript(
        "INSERT INTO usuarios (usuario, correo, clave) VALUES ('%s','%s','%s')" % (usuario, email, clave))
    #cur.execute('INSERT INTO usuario (usuario, correo, clave) VALUES (?,?,?)',(usuario, email, clave))
    print('script creado')
    conexion.commit()
    print('commit ok')
    db.close_db()
    print('creado OK')