from types import MethodType
from flask import Flask
from flask import render_template, request
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)

db = SQLAlchemy (app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fyxikzcueepluc:07cfac673c6370f6d9c25fd73e35e43f006ca53626519c24fe9fb075c78f81d5@ec2-52-86-193-24.compute-1.amazonaws.com:5432/dccpbb52b06gmr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

class Notas(db.Model):
    '''Clase Notas''' 
    _tablename_="Notas"
    idNota = db.Column(db.Integer, primary_key = True)
    tituloNota = db.Column(db.String(80))
    cuerpoNota = db.Column(db.String(150))

    def _init_(self,tituloNota,cuerpoNota):
        self.tituloNota = tituloNota
        self.cuerpoNota = cuerpoNota

@app.route('/')
def index():
    objeto = {
        "nombre": "Victor", "apellido": "Luna"
    }
    nombre = 'Victor'
    lista_nombres = ["Patricia","Memo","Cesar"]
    return render_template ("index.html", variable = lista_nombres)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/crearnota", methods=['POST'])
def crearnota():
    campotitulo = request.form ['campotitulo']
    campocuerpo = request.form ['campocuerpo']

    notaNueva = Notas (tituloNota= campotitulo,cuerpoNota=campocuerpo)
    db.session.add(notaNueva)
    db.session.commit()
    
    return redirect("/leernotas")
    #return render_template("index.html", titulo = campotitulo, cuerpo = campocuerpo)
    # return "Nota creada" + " " +campocuerpo + " " +campotitulo

@app.route("/leernotas")
def leernotas():
    consulta_notas= Notas.query.all()
    print(consulta_notas)
    for nota in consulta_notas:
        print(nota.tituloNota)
        print(nota.cuerpoNota)

    #return "Notas consultadas"
    return render_template("leerNota.html", consulta = consulta_notas)


@app.route("/eliminarnota/<ID>")
def eliminar(ID):
    nota = Notas.query.filter_by(idNota = int(ID)).delete()
    print(nota)
    db.session.commit()
    return redirect("/leernotas")

@app.route("/editarnota/<ID>")
def editar(ID):
    nota = Notas.query.filter_by(idNota = int(ID)).first()
    print(nota)
    print(nota.tituloNota)
    print(nota.cuerpoNota)
    
    return render_template("modificarNota.html", nota = nota)

@app.route("/modificarNota", methods=['POST'])
def modificarnota():
    idnota = request.form['idnota']
    ntitulo = request.form['campotitulo']
    ncuerpo = request.form['campocuerpo']
    nota = Notas.query.filter_by(idNota = int(idnota)).first()
    nota.tituloNota = ntitulo
    nota.cuerpoNota = ncuerpo
    db.session.commit()
    return redirect("/leernotas") 

if __name__ == "__main__":
    db.create_all()
    app.run()