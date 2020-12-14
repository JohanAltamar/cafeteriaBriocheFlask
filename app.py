from flask import Flask, flash, render_template, request, redirect, url_for
from markupsafe import escape
from werkzeug.utils import secure_filename
import os
import CRUD
import yagmail
import utils

UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(app.instance_path), 'static/images')
print (UPLOAD_FOLDER)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        return do_the_login()

def do_the_login():
    username = request.form["username"]
    password = request.form["password"]
    user = CRUD.buscar_un_usuario(username)
    print("==============")
    print(user)
    print("==============")
    if user == None:
        return render_template("index.html", Alert="Usuario y/o contraseña incorrectas.")
    elif user[1] == username and user[3] == password:
        if user[6]== 'True' or user[6]== 1:
            return redirect(url_for('admin'))
        else:
            if user[5] == 1 or user[5]== 'True':
                return redirect(url_for('cashier'))
            else:
                return render_template("index.html", Alert="Usuario deshabilitado, contacte al administrador.")
    else:
        return render_template("index.html", Alert="Usuario y/o contraseña incorrectas.")

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
def admin():
    return render_template('admin-dashboard.html')

@app.route("/admin/<path:subpath>")
def admin_subpaths(subpath):
    if subpath== "users":
        return render_template('admin-panel-users.html')
    elif subpath == "products":
        return render_template("admin-panel-products.html")
    elif subpath == "reports":
        return render_template("admin-panel-reports.html")

@app.route("/cashier", methods=["GET", "POST"])
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
def add_new_user_mail_sender():
    try:
        if request.method == 'POST':
            usuario=request.form['username']
            clave=request.form['password']
            email=request.form['email']
            if utils.isEmailValid(email):
                if utils.isUsernameValid(usuario):
                        if utils.isPasswordValid(clave):
                            print('todo ok, se procede a crear')
                            CRUD.register(usuario,clave,email)
                            yag=yagmail.SMTP(user='ciclo3grupof@gmail.com', password='misiontic2022') 
                            print("Email sent to: " + email)
                            yag.send(to=email,subject='Cuenta Creada',
                            contents='Sus credenciales de ingreso son las siguientes:\n -Usuario: ' + usuario + '\n -Correo: ' + email + '\n -Contraseña:' + clave)  
                            return render_template("admin-panel-users-add.html",Alert="Usuario creado correctamente. Se le envió mensaje de confirmación de cuenta a su correo.") 
                        else:
                            return render_template("admin-panel-users-add.html",Alert="Error: Clave no cumple con lo exigido.")   
                else:
                    return render_template("admin-panel-users-add.html",Alert="Error: usuario no cumple con lo exigido.")
            else:
                return render_template("admin-panel-users-add.html",Alert="Error: Correo no cumple con lo exigido.")                      
        else:
            return render_template("admin-panel-users-add.html",Alert="")
    except:
        return render_template("admin-panel-users-add.html",Alert="Ocurrió un error en la creación del usuario. Contacte al administrador de la página.")

@app.route("/admin/users/edit", methods=["GET","POST"])
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
    usuario = request.form['username']
    email = request.form['email']
    clave = request.form['password']
    enabled = request.form.get('enabled')
    if enabled == None:
        enabled = False
    if utils.isEmailValid(email) and utils.isUsernameValid(usuario) and (clave == "" or utils.isPasswordValid(clave)):
        CRUD.actualizar_usuario(userId,usuario,clave,email,enabled)
        return redirect("/admin/users/edit")
    return render_template("admin-panel-users-error.html",message="Error en la actualización del usuario. Favor verificar campos ingresados.")
    
@app.route("/admin/products/add", methods=["GET", "POST"])
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
        return render_template("admin-panel-products-error.html",message="Error en la actualización del usuario. Favor verificar campos ingresados.")

@app.route("/admin/products/search", methods=["GET","POST"])
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
    
    

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = '0'
    response.headers["Pragma"] = "no-cache"
    return response