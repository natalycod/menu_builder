from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import time
import json

import backend
from models import User, db

DAY_SECONDS = 60 * 60 * 24

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
    menu = backend.backend_get_menu(menu_id)
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

@app.route('/calendar')
def calendar_page():
    date_today = backend.get_today_date()
    return redirect(web_client_url + "/calendar/" + date_today, code=302)


@app.route('/calendar/delete_menu/<string:date>/<string:date_delete>', methods=['GET'])
def calendar_delete_menu_page(date, date_delete):
    backend.backend_calendar_delete_menu(current_user.username, date_delete)
    return redirect(web_client_url + "/calendar/" + date, code=302)


@app.route('/calendar/<string:date>', methods=['GET', 'POST'])
def calendar_date_page(date):
    if request.method == 'POST':
        date_start = request.form['date_start']
        date_end = request.form['date_end']
        return redirect(web_client_url + "/grocery_list/" + date_start + '/' + date_end, code=302)
    date_prev = backend.get_previous_date(date)
    date_next = backend.get_next_date(date)
    
    menues = backend.backend_calendar_get_menues(current_user.username, date_prev, date_next)
    menu_prev = None
    menu = None
    menu_next = None
    for menu_ in menues:
        if menu_['date'] == date_prev:
            menu_prev = menu_['menu']
        if menu_['date'] == date_next:
            menu_next = menu_['menu']
        if menu_['date'] == date:
            menu = menu_['menu']

    print(date_prev, date, date_next)
    return render_template(
        'calendar.html',
        main={
            'date': date,
            'has_menu': menu is not None,
            'menu': menu,
        },
        prev={
            'date': date_prev,
            'has_menu': menu_prev is not None,
            'menu': menu_prev,
        },
        next={
            'date': date_next,
            'has_menu': menu_next is not None,
            'menu': menu_next,
        },
        link_prev="/calendar/" + date_prev,
        link_next="/calendar/" + date_next)

@app.route('/grocery_list/<string:date_start>/<string:date_end>', methods=['GET'])
def grocery_list_page(date_start, date_end):
    grocery_list = backend.backend_calendar_get_grocery_list(current_user.username, date_start, date_end)
    return render_template('grocery_list.html', grocery_list=grocery_list)

if __name__ == '__main__':
    app.run(debug=True)
