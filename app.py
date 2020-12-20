import re
from flask import Flask, flash, render_template, request, redirect, url_for, session, make_response, jsonify, send_from_directory
import datetime
import functools
from markupsafe import escape
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import CRUD
import yagmail
import utils

UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = os.urandom( 24 ) #generamos la clave aleatoria

UPLOAD_FOLDER = os.path.join(os.path.dirname(app.instance_path), 'static/images')
print (UPLOAD_FOLDER)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#<<<<<<<<<<<<<<<<<< >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not 'user_id' in session :
            flash('Acceso denegado!')
            return redirect( url_for('index'))
        return view()
    return wrapped_view

def check_if_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get("user_admin") == 0 :
            return redirect( url_for('cashier'))
        return view()
    return wrapped_view

def check_if_cashier(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get("user_admin") == 1 :
            return redirect( url_for('admin'))
        return view()
    return wrapped_view

@app.route("/", methods=['GET', 'POST'])
@check_if_admin
@check_if_cashier
def index():
    if request.method == "GET":
        return render_template('index.html')
    return do_the_login()

def do_the_login():
    username = request.form["username"]
    password = request.form["password"]
    if not (utils.isUsernameValid(username) and utils.isPasswordValid(password)):
        return render_template("index.html", Alert="Usuario y/o contraseña incorrectas.")
    user = CRUD.buscar_un_usuario(username)
    if user is None:
        flash("Usuario y/o contraseña incorrectas.")
        return render_template("index.html", Alert="Usuario y/o contraseña incorrectas.")
    elif user[1] == username and check_password_hash(user[3], password):
        if user[5] == 1 or user[5]== 'True':
            create_session(user)
            resp = None
            if user[6]== 'True' or user[6]== 1:
                resp= make_response(redirect(url_for('admin')))
            else: 
                resp= make_response(redirect(url_for('cashier')))
            resp.set_cookie('username', username)
            userID = str(user[0])
            resp.set_cookie('userID', userID)
            return resp
        return render_template("index.html", Alert="Usuario deshabilitado, contacte al administrador.")
    return render_template("index.html", Alert="Usuario y/o contraseña incorrectas.")

def create_session(user):
    session.clear()
    session['user_id'] = user[0] #guarda el id
    session['user_login'] = user[1] #guarda el usuario
    session['user_email'] = user[2] #guarda el correo
    session['user_admin'] = user[6] #guarda si es admin

@app.route("/reset", methods=["GET", "POST"])
def reset_password():
    try:
        if request.method == 'POST':
            print("============= POST REQUEST ============")
            # usuario=request.form['usuario'] #sacar los campos del form
            # clave=request.form['clave']
            email=request.form['email']
            if utils.isEmailValid(email):
                # if utils.isUsernameValid(usuario):
                        # if utils.isPasswordValid(clave):
                yag=yagmail.SMTP(user='ciclo3grupof@gmail.com', password='misiontic2022') 
                print("Email sent to: " + email)
                yag.send(to=email,subject='Recupera tu contraseña',
                contents='Sus credenciales de ingreso son las siguientes:\n -Usuario: usuario_aqui\n -Correo: ' + email + '\n -Contraseña: tu_password')  
                return render_template('reset-password.html', RESET_OK="true")
            #             else:
            #                 return 'Error Clave no cumple con lo exigido'    
            #     else:
            #         return 'Error usuario no cumple con lo exigido'
            else:
                return 'Error Correo no cumple con lo exigido'                      
        else:
            print("================ GET request ===============")
            return render_template('reset-password.html', RESET_OK="false")
            # return 'Error faltan datos para validar'
    except:
        return "render_template('reset-password.html')"

@app.route("/admin")
@login_required
@check_if_admin
def admin():
    return render_template('admin-dashboard.html')

@app.route("/admin/<path:subpath>")
def admin_subpaths(subpath):
    check_if_admin(subpath)
    login_required(subpath)
    if subpath== "users":
        return render_template('admin-panel-users.html')
    elif subpath == "products":
        return render_template("admin-panel-products.html")
    elif subpath == "reports":
        return render_template("admin-panel-reports.html")

@app.route("/cashier", methods=["GET", "POST"])
@login_required 
@check_if_cashier
def cashier():
    if request.method == "GET":
        products = CRUD.leer_productos()
        return render_template("cashier-panel.html",products=products)
    else:
        product_name = request.form['product_name']
        products = ''
        if utils.isTextValid(product_name):
            products = CRUD.buscar_productos(product_name)
            return render_template("cashier-panel.html",products=products)
        else:
            return redirect("/cashier")   

@app.route("/admin/users/add", methods=["GET","POST"])
@login_required
@check_if_admin
def add_new_user_mail_sender():
    try:
        if request.method == 'POST':
            usuario=request.form['username']
            clave=request.form['password']
            email=request.form['email']
            if utils.isEmailValid(email):
                if utils.isUsernameValid(usuario):
                    if utils.isPasswordValid(clave):
                        ##VERIFICAR QUE EL USUARIO NO EXISTA
                        print('todo ok, se procede a crear')
                        hashed_password = generate_password_hash(clave)
                        CRUD.register(usuario,hashed_password,email)
                        yag=yagmail.SMTP(user='ciclo3grupof@gmail.com', password='misiontic2022') 
                        print("Email sent to: " + email)
                        yag.send(to=email,subject='Cuenta Creada',
                        contents='Sus credenciales de ingreso son las siguientes:\n -Usuario: ' + usuario + '\n -Correo: ' + email + '\n -Contraseña:' + clave)  
                        return render_template("admin-panel-users-add.html",Alert="Usuario creado correctamente. Se le envió mensaje de confirmación de cuenta a su correo.") 
                    return render_template("admin-panel-users-add.html",Alert="Error: Clave no cumple con lo exigido.")   
                return render_template("admin-panel-users-add.html",Alert="Error: usuario no cumple con lo exigido.")
            return render_template("admin-panel-users-add.html",Alert="Error: Correo no cumple con lo exigido.")                      
        return render_template("admin-panel-users-add.html",Alert="")
    except:
        return render_template("admin-panel-users-add.html",Alert="Ocurrió un error en la creación del usuario. Contacte al administrador de la página.")

@app.route("/admin/users/edit", methods=["GET","POST"])
@login_required
@check_if_admin
def get_modify_users():
    if request.method == 'GET':
        users = CRUD.leer_usuarios()
        if users != None:
            if iter(users):
                for user in users:
                    print(user[1])
            else:
                print(users['username'])
        return render_template("admin-panel-users-edit.html",users=users,user="")
    else:
        user = CRUD.buscar_un_usuario(request.form['username'])
        return render_template("admin-panel-users-edit.html",users="",user=user)

@app.route("/admin/users/edit/<string:userId>", methods=["POST"])
def modify_user(userId):
    login_required(userId)
    check_if_admin(userId)
    usuario = request.form['username']
    email = request.form['email']
    clave = request.form['password']
    enabled = request.form.get('enabled')
    if enabled == None:
        enabled = False
    if utils.isEmailValid(email) and utils.isUsernameValid(usuario) and (clave == "" or utils.isPasswordValid(clave)):
        hashed_password=generate_password_hash(clave)
        CRUD.actualizar_usuario(userId,usuario,hashed_password,email,enabled)
        return redirect("/admin/users/edit")
    return render_template("admin-panel-users-error.html",message="Error en la actualización del usuario. Favor verificar campos ingresados.")
    
@app.route("/admin/products/add", methods=["GET", "POST"])
@login_required
@check_if_admin
def add_new_product():
    if request.method == "GET":
        return render_template("admin-panel-products-add.html")
    else:
        print (request.files)
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = file.filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product_name = request.form['product_name']
            product_price = request.form['product_price']
            CRUD.create_product(product_name,product_price,filename)
            return render_template("admin-panel-products-add.html",Alert="Producto creado exitosamente.")
        return render_template("admin-panel-products-add.html")

@app.route("/admin/products/edit", methods=["GET","POST"])
@login_required
@check_if_admin
def get_modify_products():
    if request.method == 'GET':
        products = CRUD.leer_productos()
        print(products)
        if products != None:
            if iter(products):
                for product in products:
                    print(product[1])
            else:
                print(products['product_name'])
        return render_template("admin-panel-products-edit.html",products=products,product="")
    else:
        product = CRUD.buscar_un_producto(request.form['product_name'])
        return render_template("admin-panel-products-edit.html",products="",product=product)

@app.route("/admin/products/edit/<string:productId>", methods=["POST"])
def modify_product(productId):
    login_required(productId)
    check_if_admin(productId)
    product_name = request.form['product_name']
    product_price = request.form['product_price']
    enabled = request.form.get('enabled')
    if enabled == None:
        enabled = False
    try:
        product_filename=""
        if 'file' not in request.files:
            print('No file part')
        else:
            file = request.files['file']
            if file.filename == '':
                print('No selected file')
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                product_filename=filename
        CRUD.actualizar_producto(productId,product_name,product_price,product_filename,enabled)
        return redirect("/admin/products/edit")
    except:
        return render_template("admin-panel-products-error.html",message="Error en la actualización del producto. Favor verificar campos ingresados.")

@app.route("/admin/products/search", methods=["GET","POST"])
@login_required
@check_if_admin
def search_products():
    if request.method == "GET":
        products = CRUD.leer_productos()
    else:
        product_name = request.form['product_name']
        products = ''
        if utils.isTextValid(product_name):
            products = CRUD.buscar_productos(product_name)
        else:
            return redirect("/admin/products/search")
    return render_template("admin-panel-products-search.html",products=products)
    
@app.route("/logout")
def logout_user():
    session.clear()
    return redirect("/")

@app.route("/products")
def fetchProducts():
    product_name = request.args["name"]
    print(product_name)
    if product_name:
        res = CRUD.buscar_productos(product_name)
        return jsonify(res)
    res = CRUD.leer_productos()
    return jsonify(res)

@app.route("/get-image")
def getImage():
    product_image=request.args["image"]
    print(product_image)
    if product_image:
        return send_from_directory(UPLOAD_FOLDER, filename=product_image)

@app.route("/add-product-to-order/<product_id>", methods=['POST'])
def addProductToOrder (product_id): 
    if(request.method == 'POST'):
        currentOrder = CRUD.buscar_orden(session.get('user_id'))
        print(currentOrder)
        # buscar si el usuario tiene alguna orden disponible 
        if len(currentOrder) == 0:
            now = datetime.datetime.now()
            CRUD.create_order(session.get('user_id'), now, 0)
            currentOrder = CRUD.buscar_orden(session.get('user_id'))
            print(currentOrder)
        order_id = currentOrder[0][0]

        #buscar si el producto ya existe en la orden
        product_in_order = CRUD.buscar_producto_en_orden(product_id, order_id)
        print(product_in_order)

        #buscar información del producto
        product_info = CRUD.buscar_un_producto(None, product_id)
        product_price = product_info[2]

        #agregar productos a tabla detalles o modificarlos
        if product_in_order is None:
            CRUD.add_product_to_order(product_id, order_id, 1, product_price)
        else:
            CRUD.update_product_in_order(product_id, order_id)
        
        
        update_order_total(order_id)


        # return jsonify({"order_id": currentOrder[0][0], "user_id": currentOrder[0][1], "payment_method_id": currentOrder[0][2], "order_date": currentOrder[0][3], "order_total":currentOrder[0][4], "order_open": currentOrder[0][5]})
        products_in_order = CRUD.get_order_complete_info(order_id)
        return jsonify(products_in_order)

def update_order_total(order_id):
    items_in_order = CRUD.leer_detalles_orden(order_id)
    total = 0
    for item in items_in_order:
        total += item[3]*item[4]
    now = datetime.datetime.now()
    CRUD.update_order_total(order_id,total,now)



@app.route("/sub-product-from-order/<product_id>", methods=['POST'])
def subProductFromOrder (product_id): 
    if(request.method == 'POST'):
        currentOrder = CRUD.buscar_orden(session.get('user_id'))
        order_id = currentOrder[0][0]
        product_in_order = CRUD.buscar_producto_en_orden(product_id, order_id)
        print(product_in_order)
        if (product_in_order[4]>1):
            CRUD.substract_product_qty_in_order(product_id,order_id)
        else:
            CRUD.delete_product_from_order(product_id,order_id)
        update_order_total(order_id)    
        products_in_order = CRUD.get_order_complete_info(order_id)
        return jsonify(products_in_order)

@app.route("/get-order-info")
def getOrdersInfo():
    currentOrder = CRUD.buscar_orden(session.get('user_id'))
    if not currentOrder:
        return {}
    order_id = currentOrder[0][0]
    products_in_order = CRUD.get_order_complete_info(order_id)
    return jsonify(products_in_order)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = '0'
    response.headers["Pragma"] = "no-cache"
    return response