from flask import Flask, request, flash, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cuadrangular.sqlite3'
app.config['SECRET_KEY'] = "123456789"

db = SQLAlchemy(app)
inspector = inspect(db.engine)
schemas = inspector.get_schema_names()
metadata = MetaData()


class t_clasificacion(db.Model):
    id = db.Column('e_id', db.Integer, primary_key=True)
    e_nombre = db.Column(db.String(100))
    e_partidosj = db.Column(db.Integer)
    e_puntos = db.Column(db.Integer)
    e_golesf = db.Column(db.Integer)
    e_golesc = db.Column(db.Integer)
    e_difgoles = db.Column(db.Integer)

    def __init__(self, nombre, partidosj, puntos, golesf, golesc, difgoles):
        self.e_nombre = nombre
        self.e_partidosj = partidosj
        self.e_puntos = puntos
        self.e_golesf = golesf
        self.e_golesc = golesc
        self.e_difgoles = difgoles


class historico(db.Model):
    id = db.Column('h_id', db.Integer, primary_key=True)
    h_E1 = db.Column(db.String(100))
    h_golesE1 = db.Column(db.Integer)
    h_E2 = db.Column(db.Integer)
    h_golesE2 = db.Column(db.Integer)

    def __init__(self):
        self.h_E1 = equipo1
        self.h_E2 = equipo2
        self.h_golesE1 = golesequipo1
        self.h_golesE2 = golesequipo2


@app.route('/')
def index():
    entidades = db.engine.table_names()
    return render_template('index.html', entidades=entidades)


@app.route('/registraequipos/<entidad>', methods=["POST", "GET"])
def confirmar(entidad):
    campos = inspector.get_columns(entidad)
    valores = []
    if request.method == "POST":

        valores.append(request.form["E1"])
        valores.append(request.form["E2"])
        valores.append(request.form["E3"])
        valores.append(request.form["E4"])

        for table_name in metadata.tables.keys():
            if table_name == entidad:
                for i in range(0, 4):
                    inst = "INSERT INTO "+table_name+" ("
                    for campo in range(len(campos)-1):
                        inst = inst+str(campos[campo]['name'])+", "
                    inst = inst + \
                        str(campos[len(campos)-1]['name']) + ") VALUES ("
                    inst = inst+"'"+str(i)+"', '" + \
                        valores[i]+"', '0', '0', '0', '0', '0');"
                    # for valor in range(1, len(valores)-1):
                    #    inst = inst+"'"+str(valores[valor])+"'"+", "
                    # inst = inst + "'"+str(valores[len(valores)-1])+"'" + ");"
                    # print(inst)
                    # db.engine.execute("INSERT INTO categoria (cat_id, cat_nombre, cat_tipo) VALUES ('1', 'nombreprueba1', '1')")
                    db.engine.execute(inst)
        registros = db.engine.execute("SELECT e_nombre FROM "+entidad+" ;")
        registros = registros.fetchall()
        return render_template('partidos.html', entidad=entidad, campos=campos, registros=registros)
    else:
        return render_template('falla.html')


@app.route('/procesa/<partidonum>', methods=["POST", "GET"])
def procesapartido(partidonum):
    if request.method == "POST":
        entidad = 't_clasificacion'
        campos = inspector.get_columns(entidad)
        nombre_e1 = request.form["nombre_e1"]
        nombre_e2 = request.form["nombre_e2"]

        registros_e1 = db.engine.execute(
            "SELECT * FROM "+entidad+" WHERE "+str(campos[1]['name'])+" IN ('"+nombre_e1+"');")
        registros_e1 = registros_e1.fetchall()

        registros_e2 = db.engine.execute(
            "SELECT * FROM "+entidad+" WHERE "+str(campos[1]['name'])+" IN ('"+nombre_e2+"');")
        registros_e2 = registros_e2.fetchall()

        goles_e1 = request.form['goles_e1']
        goles_e2 = request.form['goles_e2']

        if(goles_e1 > goles_e2):
            valores = {'equipo1': [registros_e1[0][0], registros_e1[0][1], int(registros_e1[0][2])+3, int(registros_e1[0][3])+int(goles_e1), int(registros_e1[0][4])+int(goles_e2), int(registros_e1[0][5])+(int(registros_e1[0][3])+int(goles_e1)-int(registros_e1[0][4])+int(goles_e2))],
                    'equipo2': [registros_e2[0][0], registros_e2[0][1], int(registros_e2[0][2])+0, int(registros_e2[0][3])+int(goles_e2), int(registros_e2[0][4])+int(goles_e1), int(registros_e2[0][5])+(int(registros_e2[0][3])+int(goles_e2)-int(registros_e2[0][4])+int(goles_e1))]}
        elif(goles_e2 > goles_e1):
             valores={'equipo1': [registros_e1[0][0], registros_e1[0][1], int(registros_e1[0][2])+0, int(registros_e1[0][3])+int(goles_e1), int(registros_e1[0][4])+int(goles_e2), int(registros_e1[0][5])+(int(registros_e1[0][3])+int(goles_e1)-int(registros_e1[0][4])+int(goles_e2))],
                    'equipo2': [registros_e2[0][0], registros_e2[0][1], int(registros_e2[0][2])+3, int(registros_e2[0][3])+int(goles_e2), int(registros_e2[0][4])+int(goles_e1), int(registros_e2[0][5])+(int(registros_e2[0][3])+int(goles_e2)-int(registros_e2[0][4])+int(goles_e1))]}
        elif(goles_e1 == goles_e2):
             valores={'equipo1': [registros_e1[0][0], registros_e1[0][1], int(registros_e1[0][2])+1, int(registros_e1[0][3])+int(goles_e1), int(registros_e1[0][4])+int(goles_e2), int(registros_e1[0][5])+(int(registros_e1[0][3])+int(goles_e1)-int(registros_e1[0][4])+int(goles_e2))],
                    'equipo2': [registros_e2[0][0], registros_e2[0][1], int(registros_e2[0][2])+1, int(registros_e2[0][3])+int(goles_e2), int(registros_e2[0][4])+int(goles_e1), int(registros_e2[0][5])+(int(registros_e2[0][3])+int(goles_e2)-int(registros_e2[0][4])+int(goles_e1))]}
        else:
            pass

        inst="UPDATE "+entidad+" SET "
        for campo in range(1, len(campos)-1):
            inst=inst+str(campos[campo]['name']) +"='"+str(valores['equipo1'][campo])+"', "
        inst = inst + str(campos[len(campos)-1]['name']) + \
            "='"+str(valores['equipo1'][len(valores['equipo1'])-1])+"' WHERE "
        inst = inst + str(campos[0]['name'])+"="+str(valores['equipo1'][0])+";"
        print(inst)
        db.engine.execute(inst)

        inst="UPDATE "+entidad+" SET "
        for campo in range(1, len(campos)-1):
            inst=inst+str(campos[campo]['name']) +"='"+str(valores['equipo2'][campo])+"', "
        inst = inst + str(campos[len(campos)-1]['name']) + \
            "='"+str(valores['equipo2'][len(valores['equipo2'])-1])+"' WHERE "
        inst = inst + str(campos[0]['name'])+"="+str(valores['equipo2'][0])+";"
        print(inst)
        db.engine.execute(inst)
        # for campo in campos:
        #    if campo['name'] == nombre_e1:
        #        print(nombre_e1)
        #        registros = db.engine.execute(
        #            "SELECT * FROM "+entidad+" WHERE "+str(campo['name'])+" IN ('"+idact+"');")
        #        registros = registros.fetchall()

        # goles_e1 = request.form['goles_e1']
        # goles_e2 = request.form['goles_e2']

        # if(goles_e1 > goles_e2)
        # valores = {'equipo1': [request.form['goles_e1'], request.form['nombre_e1'], ],
        #           'equipo2': [request.form['goles_e2'], request.form['nombre_e2']]}
        return render_template("confirmacion.html")
    else:
        return render_template("falla.html")


def list(entidad):
    campos=inspector.get_columns(entidad)
    registros=db.engine.execute("SELECT e_nombre FROM "+entidad+" ;")
    registros=registros.fetchall()
    return registros


if __name__ == '__main__':

    # Si se quiere mantener la sesion anterior hay que evitar que se borre todo en la base de datos
    db.drop_all()
    db.create_all()
    metadata=db.metadata
    # print(metadata.tables.keys())

    app.run('localhost', 8000, debug=True)
