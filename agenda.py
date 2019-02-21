import os
import re

from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy

bp = Blueprint('agenda', __name__)

# create and configure the app
app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))
app.config.from_mapping(
    SECRET_KEY='dev',
)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)

class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), unique=False, nullable=False)
    apellido = db.Column(db.String(100), unique=False, nullable=True)
    email = db.Column(db.String(100), unique=False, nullable=True)
    numero = db.Column(db.String(20), unique=False, nullable=False)
    tipo = db.Column(db.String(10), unique=False, nullable=True)

    def __repr__(self):
        return '<Registro %r>' % self.nombre

# a simple page that says hello
@app.route('/hello')
def hello():
    return 'Hello, World!'

@bp.route('/', methods=('GET', 'POST'))
def index():
    numeros = Registro.query.all()
    return render_template('agenda/index.html', numeros=numeros)

@bp.route('/create',  methods=('POST',))
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        numero = request.form['numero']
        tipo = request.form['tipo']
        error = None

        if not nombre:
            error = 'El nombre es necesario \n'
        if not numero:
            if error is None:
                error = 'El numero de telefono es requerido \n'
            else:
                error += 'El numero de telefono es requerido \n'
        if not re.match(r"[^@]+@[^@]+\.[^@]+", direccion):
            if error is None:
                error = 'EL email no es valido \n'
            else:
                error += 'EL email no es valido \n'
        if error is not None:
            flash(error)
        else:
            try:
                registro = Registro(nombre = nombre, apellido = apellido, email = direccion, numero = numero, tipo = tipo)
                print(registro)
                db.session.add(registro)
                db.session.commit()
            except Exception as e:
                flash("No se pudo agregar ")
            return redirect(url_for('agenda.index'))
    return index()

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion'] 
        numero = request.form['numero']
        tipo = request.form['tipo']
        error = None

        if not nombre:
            error = 'El nombre es necesario \n'
        if not numero:
            if error is None:
                error = 'El numero de telefono es requerido \n'
            else:
                error += 'El numero de telefono es requerido \n'
        if not re.match(r"[^@]+@[^@]+\.[^@]+", direccion):
            if error is None:
                error = 'EL email no es valido \n'
            else:
                error += 'EL email no es valido \n'
        if error is not None:
            flash(error)
        else:
            
            registro = Registro.query.filter_by(id = id).first()
            registro.nombre = nombre
            registro.apellido = apellido
            registro.email = direccion
            registro.numero = numero
            registro.tipo = tipo
            db.session.commit()
            return redirect(url_for('agenda.index'))
    registro = Registro.query.filter_by(id = id).first()
    return render_template('agenda/update.html', registro=registro)

@bp.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    registro = Registro.query.filter_by(id=id).first()
    db.session.delete(registro)
    db.session.commit()
    return index()   

app.register_blueprint(bp)
app.add_url_rule('/', endpoint='index')

if __name__ == "__main__":
    app.run(debug=True)