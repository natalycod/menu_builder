from flask import Flask, render_template, request, redirect
import json
import requests
# from models import Book, db

server_url = "http://127.0.0.1:6000"
web_client_url = "http://127.0.0.1:5000"

def backend_build_menu(args, menu_prev):
    req = {
        "calories": [1000]
    }
    if 'breakfast_fixed' in args and args['breakfast_fixed'] == 'true':
        req['breakfast_id'] = menu_prev['breakfast_info']['recipe_id']
    if 'lunch_fixed' in args and args['lunch_fixed'] == 'true':
        req['lunch_id'] = menu_prev['lunch_info']['recipe_id']
    if 'dinner_fixed' in args and args['dinner_fixed'] == 'true':
        req['dinner_id'] = menu_prev['dinner_info']['recipe_id']
    
    print("natalycod_debug: request = ", req)
    response = requests.post(server_url + "/build_menu", json=req)
    return json.loads(response.text)

def backend_get_menu(menu_id):
    url = server_url + "/get_menu?menu_id=" + menu_id
    response = requests.get(url)
    return json.loads(response.text)

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
    menu = backend_get_menu(menu_id)
    return render_template('build_menu_with_id.html', menu=menu, args=request.args)

@app.route('/build_menu/hi')
def build_menu_hi():
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
        menu_prev = backend_get_menu(request.args['menu_id'])
    menu_js = backend_build_menu(request.args, menu_prev)
    return redirect(web_client_url + "/build_menu/" + menu_js['id'] + params, code=302)

if __name__ == '__main__':
    app.run(debug=True)
