import db
def register(usuario,clave,email):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("INSERT INTO users (username, email, password, enabled) VALUES (?,?,?,'True')" , [usuario, email, clave])
    connection.commit()
    db.close_db()

def leer_usuarios():
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("SELECT * FROM users")
    rv = cur.fetchall()
    db.close_db()
    return rv

def buscar_un_usuario(username):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", [username])
    rv = cur.fetchone()
    db.close_db()
    return rv

def buscar_un_correo(email):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", [email])
    rv = cur.fetchone()
    db.close_db()
    return rv

def actualizar_usuario(id,usuario,clave,email,enabled):
    connection = db.get_db()
    cur=connection.cursor()
    if clave == "":
        cur.execute("UPDATE users SET username=?, email=?, enabled=? WHERE id=?" , [usuario, email, enabled, id])
    else:
        cur.execute("UPDATE users SET username=?, email=?, password=?, enabled=? WHERE id=?" , [usuario, email, clave, enabled, id])
    connection.commit()
    db.close_db()

def create_product(product_name,product_price,filename):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("INSERT INTO products (product_name, product_price, product_filename,enabled) VALUES (?,?,?,'True')" , [product_name, product_price, filename])
    connection.commit()
    db.close_db()

def leer_productos():
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("SELECT * FROM products")
    rv = cur.fetchall()
    db.close_db()
    return rv

def buscar_un_producto(product_name, product_id):
    connection = db.get_db()
    cur=connection.cursor()
    if product_name is not None:
        cur.execute("SELECT * FROM products WHERE product_name = ?", [product_name])
    else:
        cur.execute("SELECT * FROM products WHERE id = ?", [product_id])
    rv = cur.fetchone()
    db.close_db()
    return rv

def buscar_productos(product_name):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute(f"SELECT * FROM products WHERE product_name LIKE '%{product_name}%'")
    rv = cur.fetchall()
    db.close_db()
    return rv

def actualizar_producto(id,product_name,product_price,product_filename,enabled):
    connection = db.get_db()
    cur=connection.cursor()
    if product_filename == "":
        cur.execute("UPDATE products SET product_name=?, product_price=?, enabled=? WHERE id=?" , [product_name, product_price, enabled, id])
    else:
        cur.execute("UPDATE products SET product_name=?, product_price=?, product_filename=?, enabled=? WHERE id=?" , [product_name, product_price, product_filename,enabled, id])
    connection.commit()
    db.close_db()

def create_order(user_id, order_date, order_total):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("INSERT INTO orders (user_id, order_date, order_total, order_open) VALUES (?,?,?, 1)" , [user_id, order_date, order_total])
    connection.commit()
    db.close_db()

def buscar_orden(user_id):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("SELECT * FROM orders WHERE user_id= ? AND order_open= ?", (user_id, 1))
    rv = cur.fetchall()
    db.close_db()
    return rv

def add_product_to_order(product_id, order_id, product_qty, product_price):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("INSERT INTO details (product_id, order_id, product_price, product_qty) VALUES (?, ?, ?, ?)" , [product_id, order_id, product_price, product_qty])
    connection.commit()
    db.close_db()

def buscar_producto_en_orden(product_id, order_id):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("SELECT * FROM details WHERE product_id = ? AND order_id= ?", (product_id, order_id))
    rv = cur.fetchone()
    db.close_db()
    return rv

def leer_detalles_orden(order_id):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("SELECT * FROM details WHERE order_id= ?", [order_id])
    rv = cur.fetchall()
    db.close_db()
    return rv

def update_product_in_order(product_id, order_id):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("UPDATE details SET product_qty= product_qty + 1 WHERE order_id= ? AND product_id= ?" , [order_id, product_id])
    connection.commit()
    db.close_db()

def substract_product_qty_in_order(product_id, order_id):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("UPDATE details SET product_qty= product_qty - 1 WHERE order_id= ? AND product_id= ?" , [order_id, product_id])
    connection.commit()
    db.close_db()

def delete_product_from_order(product_id,order_id):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("DELETE FROM details WHERE order_id= ? AND product_id= ?" , [order_id, product_id])
    connection.commit()
    db.close_db()

def update_order_total(order_id, order_total, order_date):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("UPDATE orders SET order_total= ?, order_date= ? WHERE id= ? " , [order_total, order_date, order_id])
    connection.commit()
    db.close_db()

def get_order_complete_info(order_id):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("""SELECT DISTINCT details.order_id, details.product_id, products.product_name, products.product_price, details.product_qty,  orders.order_date, orders.order_total
    FROM details, products, orders  
    WHERE orders.id = ?
    AND details.product_id=products.id 
    AND details.order_id=orders.id""", [order_id])
    rv = cur.fetchall()
    db.close_db()
    return rv

def order_checkout(order_id, order_date):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("UPDATE orders SET order_open= 0, order_date= ? WHERE id= ? " , [order_date, order_id])
    connection.commit()
    db.close_db()

def get_orders_from_date(order_date):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("SELECT orders.id,orders.order_total,username FROM orders INNER JOIN users ON orders.user_id=users.id WHERE order_date >= ? AND order_date < ? AND order_open = 0",[order_date,order_date + " 23:59:59.999"])
    rv = cur.fetchall()
    db.close_db()
    return rv

def create_recovery_data(user_id,recovery_key,recovery_date):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("INSERT INTO email_recovery (user_id, recovery_key, recovery_date) VALUES (?,?,?)" , [user_id, recovery_key, recovery_date])
    connection.commit()
    db.close_db()

def check_recovery_data(recoveryKey):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("SELECT * FROM email_recovery WHERE recovery_key = ? AND used = 0", [recoveryKey])
    rv = cur.fetchone()
    db.close_db()
    return rv

def update_password_recovery(user_id,password):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("UPDATE users SET password=? WHERE id=?" , [password, user_id])
    connection.commit()
    db.close_db()

def set_used_recovery_data(user_id):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("UPDATE email_recovery SET used=1 WHERE user_id=?" , [user_id])
    connection.commit()
    db.close_db()    

def delete_cart_items(order_id):
    connection = db.get_db()
    cur=connection.cursor()
    cur.execute("DELETE FROM details WHERE order_id= ?" , [order_id])
    connection.commit()
    db.close_db()