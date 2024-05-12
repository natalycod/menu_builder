from flask import Flask, render_template, request, redirect
import json
import requests

import backend

# from models import Book, db

web_client_url = "http://127.0.0.1:5000"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# связываем приложение и экземпляр SQLAlchemy
# db.init_app(app)

@app.route('/')
def index():
    return "Main Page"

@app.route('/menu/<string:menu_id>')
def menu_page(menu_id):
    f = open("test_data/menu.json")
    menu = json.load(f)
    f.close()
    return render_template('menu.html', menu=menu)

@app.route('/build_menu')
def build_menu_page():
    return render_template('build_menu.html')

@app.route('/build_menu/<string:menu_id>')
def build_menu_page_with_id(menu_id):
    menu = backend.backend_get_menu(menu_id)
    grocery_list = backend.backend_menu_get_grocery_list(menu_id)
    return render_template('build_menu_with_id.html', menu=menu, grocery_list=grocery_list, args=request.args)

@app.route('/build_menu/gen')
def build_menu_gen():
    params = ""
    if 'breakfast_fixed' in request.args:
        params += "?breakfast_fixed=" + request.args['breakfast_fixed']
    else:
        params += "?breakfast_fixed=false"
    
    if 'lunch_fixed' in request.args:
        params += "&lunch_fixed=" + request.args['lunch_fixed']
    else:
        params += "&lunch_fixed=false"

    if 'dinner_fixed' in request.args:
        params += "&dinner_fixed=" + request.args['dinner_fixed']
    else:
        params += "&dinner_fixed=false"
    
    menu_prev = None
    if 'menu_id' in request.args:
        menu_prev = backend.backend_get_menu(request.args['menu_id'])
    menu_js = backend.backend_build_menu(request.args, menu_prev)
    return redirect(web_client_url + "/build_menu/" + menu_js['id'] + params, code=302)

if __name__ == '__main__':
    app.run(debug=True)
