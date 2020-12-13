import db
def register(usuario,clave,email):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.executescript("INSERT INTO users (username, email, password) VALUES ('%s','%s','%s')" % (usuario, email, clave))
    conexion.commit()
    db.close_db()

def leer_usuarios():
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute("SELECT * FROM users")
    rv = cur.fetchall()
    db.close_db()
    return rv

def buscar_un_usuario(username):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute("SELECT * FROM users WHERE username = '" + username + "'")
    rv = cur.fetchone()
    db.close_db()
    return rv

def actualizar_usuario(id,usuario,clave,email,enabled):
    conexion = db.get_db()
    cur=conexion.cursor()
    if clave == "":
        cur.executescript("UPDATE users SET username='%s', email='%s', enabled='%s' WHERE id='%s'" % (usuario, email, enabled, id))
    else:
        cur.executescript("UPDATE users SET username='%s', email='%s', password='%s', enabled='%s' WHERE id='%s'" % (usuario, email, clave, enabled, id))
    conexion.commit()
    db.close_db()