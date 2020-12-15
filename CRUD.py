import db
def register(usuario,clave,email):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.executescript("INSERT INTO users (username, email, password, enabled) VALUES ('%s','%s','%s','True')" % (usuario, email, clave))
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

def login_usuario(username, password):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
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

def create_product(product_name,product_price,filename):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.executescript("INSERT INTO products (product_name, product_price, product_filename,enabled) VALUES ('%s','%s','%s','True')" % (product_name, product_price, filename))
    conexion.commit()
    db.close_db()

def leer_productos():
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute("SELECT * FROM products")
    rv = cur.fetchall()
    db.close_db()
    return rv

def buscar_un_producto(product_name):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute("SELECT * FROM products WHERE product_name = '" + product_name + "'")
    rv = cur.fetchone()
    db.close_db()
    print(rv)
    return rv

def buscar_productos(product_name):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute("SELECT * FROM products WHERE product_name LIKE '%" + product_name + "%'")
    rv = cur.fetchall()
    db.close_db()
    print(rv)
    return rv

def actualizar_producto(id,product_name,product_price,product_filename,enabled):
    conexion = db.get_db()
    cur=conexion.cursor()
    if product_filename == "":
        cur.executescript("UPDATE products SET product_name='%s', product_price='%s', enabled='%s' WHERE id='%s'" % (product_name, product_price, enabled, id))
    else:
        cur.executescript("UPDATE products SET product_name='%s', product_price='%s', product_filename='%s', enabled='%s' WHERE id='%s'" % (product_name, product_price, product_filename,enabled, id))
    conexion.commit()
    db.close_db()