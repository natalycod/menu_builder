from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import json
import requests

import backend
from models import User, db

# from models import Book, db

web_client_url = "http://127.0.0.1:5000"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    else:
        return render_template('index.html')

@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html', user=current_user)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        calories = request.form['calories']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already taken')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, email=email, calories=calories)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully')
            return redirect(url_for('login'))
    return render_template('register.html')

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
    menu_js = backend.backend_build_menu(request.args, menu_prev, current_user.calories)
    return redirect(web_client_url + "/build_menu/" + menu_js['id'] + params, code=302)

@app.route('/save_menu/<string:menu_id>', methods=['GET', 'POST'])
def save_menu(menu_id):
    if request.method == 'POST':
        date = request.form['date']
        backend.backend_calendar_save_menu(current_user.username, date, menu_id)
        return redirect(web_client_url + "/build_menu", code=302)
    menu = backend.backend_get_menu(menu_id)
    return render_template('save_menu.html', menu=menu)

if __name__ == '__main__':
    app.run(debug=True)
