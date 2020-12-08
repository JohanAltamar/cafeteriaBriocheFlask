from flask import Flask, render_template, request,redirect, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('index.html')
    else:
        return do_the_login()

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

@app.route("/reset")
def reset():
    return render_template('reset-password.html')

def do_the_login():
    print("Haciendo login")
    return redirect(url_for('admin'))

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = '0'
    response.headers["Pragma"] = "no-cache"
    return response