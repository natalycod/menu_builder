from flask import Flask, render_template
import json
# from models import Book, db

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

if __name__ == '__main__':
    app.run(debug=True)
