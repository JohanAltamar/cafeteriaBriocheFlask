import db
def register(usuario,clave,email):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute("INSERT INTO users (username, email, password, enabled) VALUES (?,?,?,'True')" , [usuario, email, clave])
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
    cur.execute("SELECT * FROM users WHERE username = ?", [username])
    rv = cur.fetchone()
    db.close_db()
    return rv


def actualizar_usuario(id,usuario,clave,email,enabled):
    conexion = db.get_db()
    cur=conexion.cursor()
    if clave == "":
        cur.execute("UPDATE users SET username=?, email=?, enabled=? WHERE id=?" , [usuario, email, enabled, id])
    else:
        cur.execute("UPDATE users SET username=?, email=?, password=?, enabled=? WHERE id=?" , [usuario, email, clave, enabled, id])
    conexion.commit()
    db.close_db()

def create_product(product_name,product_price,filename):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute("INSERT INTO products (product_name, product_price, product_filename,enabled) VALUES (?,?,?,'True')" , [product_name, product_price, filename])
    conexion.commit()
    db.close_db()

def leer_productos():
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute("SELECT * FROM products")
    rv = cur.fetchall()
    db.close_db()
    return rv

def buscar_un_producto(product_name, product_id):
    conexion = db.get_db()
    cur=conexion.cursor()
    if product_name is not None:
        cur.execute("SELECT * FROM products WHERE product_name = ?", [product_name])
    else:
        cur.execute("SELECT * FROM products WHERE id = ?", [product_id])
    rv = cur.fetchone()
    db.close_db()
    print(rv)
    return rv

def buscar_productos(product_name):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute(f"SELECT * FROM products WHERE product_name LIKE '%{product_name}%'")
    rv = cur.fetchall()
    db.close_db()
    print(rv)
    return rv

def actualizar_producto(id,product_name,product_price,product_filename,enabled):
    conexion = db.get_db()
    cur=conexion.cursor()
    if product_filename == "":
        cur.execute("UPDATE products SET product_name=?, product_price=?, enabled=? WHERE id=?" , [product_name, product_price, enabled, id])
    else:
        cur.execute("UPDATE products SET product_name=?, product_price=?, product_filename=?, enabled=? WHERE id=?" , [product_name, product_price, product_filename,enabled, id])
    conexion.commit()
    db.close_db()

def create_order(user_id, order_date, order_total):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute("INSERT INTO orders (user_id, order_date, order_total, order_open) VALUES (?,?,?, 1)" , [user_id, order_date, order_total])
    conexion.commit()
    db.close_db()

def buscar_orden(user_id):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute("SELECT * FROM orders WHERE user_id= ? AND order_open= ?", (user_id, 1))
    rv = cur.fetchall()
    db.close_db()
    return rv

def add_product_to_order(product_id, order_id, product_qty, product_price):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute("INSERT INTO details (product_id, order_id, product_price, product_qty) VALUES (?, ?, ?, ?)" , [product_id, order_id, product_price, product_qty])
    conexion.commit()
    db.close_db()

def buscar_producto_en_orden(product_id, order_id):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute("SELECT * FROM details WHERE product_id = ? AND order_id= ?", (product_id, order_id))
    rv = cur.fetchone()
    db.close_db()
    return rv

def update_product_in_order(product_id, order_id):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute("UPDATE details SET product_qty= product_qty + 1 WHERE order_id= ? AND product_id= ?" , [order_id, product_id])
    conexion.commit()
    db.close_db()

def update_order_total(order_id, product_price, order_date):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute("UPDATE orders SET order_total= order_total + ?, order_date= ? WHERE id= ? " , [product_price, order_date, order_id])
    conexion.commit()
    db.close_db()

def get_order_complete_info(order_id):
    conexion = db.get_db()
    cur=conexion.cursor()
    cur.execute("""SELECT DISTINCT details.order_id, details.product_id, products.product_name, products.product_price, details.product_qty,  orders.order_date, orders.order_total
    FROM details, products, orders  
    WHERE orders.id = ?
    AND details.product_id=products.id 
    AND details.order_id=orders.id""", [order_id])
    rv = cur.fetchall()
    db.close_db()
    return rv