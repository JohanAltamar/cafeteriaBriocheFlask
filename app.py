from flask import Flask, render_template, request,redirect, url_for
from markupsafe import escape
import yagmail
import utils

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        return do_the_login()

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
                return 'revisa tu correo='+email
            #             else:
            #                 return 'Error Clave no cumple con lo exigido'    
            #     else:
            #         return 'Error usuario no cumple con lo exigido'
            else:
                return 'Error Correo no cumple con lo exigido'                      
        else:
            print("================ GET request ===============")
            return render_template('reset-password.html')
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
    elif subpath == "users/add":
        return render_template("admin-panel-users-add.html")
    elif subpath == "users/edit":
        return render_template("admin-panel-users-edit.html")
    elif subpath == "products":
        return render_template("admin-panel-products.html")
    elif subpath == "products/add":
        return render_template("admin-panel-products-add.html")
    elif subpath == "products/edit":
        return render_template("admin-panel-products-edit.html")
    elif subpath == "products/search":
        return render_template("admin-panel-products-search.html")
    elif subpath == "reports":
        return render_template("admin-panel-reports.html")

@app.route("/cashier")
def cashier():
    return render_template("cashier-panel.html")

def do_the_login():
    print("Haciendo login")
    return redirect(url_for('admin'))

@app.route("/add_new_user", methods=["POST"])
def add_new_user_mail_sender():
    try:
        if request.method == 'POST':
            usuario=request.form['username'] #sacar los campos del form
            clave=request.form['password']
            email=request.form['email']
            if utils.isEmailValid(email):
                if utils.isUsernameValid(usuario):
                        if utils.isPasswordValid(clave):
                            yag=yagmail.SMTP(user='ciclo3grupof@gmail.com', password='misiontic2022') 
                            print("Email sent to: " + email)
                            yag.send(to=email,subject='Cuenta Creada',
                            contents='Sus credenciales de ingreso son las siguientes:\n -Usuario: ' + usuario + '\n -Correo: ' + email + '\n -Contraseña:' + clave)  
                            return 'revisa tu correo='+email
                        else:
                            return 'Error Clave no cumple con lo exigido'    
                else:
                    return 'Error usuario no cumple con lo exigido'
            else:
                return 'Error Correo no cumple con lo exigido'                      
        else:
            # return render_template('reset-password.html')
            return 'Error faltan datos para validar'
    except:
        return "Ocurrió un error"

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = '0'
    response.headers["Pragma"] = "no-cache"
    return response