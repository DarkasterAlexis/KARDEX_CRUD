from flask import Flask,render_template,redirect,url_for,request
import sqlite3
app = Flask(__name__)

#Creacion de la base de datos
def init_database():
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute(
        """
         CREATE TABLE IF NOT EXISTS personas(
             id INTEGER PRIMARY KEY,
             nombre TEXT NOT NULL, 
             telefono TEXT NOT NULL,
             fecha_nac DATE NOT NULL 
         )
        """
    )
    
    # cursor.execute(
    #     """
    #     INSERT INTO personas (nombre,telefono,fecha_nac)
    #     VALUES 
    #     ('Nidia Guadalupe','61535166','2000-03-13'),
    #     ('Bruno Diaz','35235243','1995-10-11'),
    #     ('Alan Brito','54254544','200-10-15'),
    #     ('Maritzabel','25468544','2023-05-14')
    #     """
    # )
    
    # cursor.execute("DROP TABLE IF EXISTS personas")
    
    conn.commit()
    conn.close()
init_database()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/personas")
def personas():
    conn = sqlite3.connect("kardex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas")
    personas = cursor.fetchall()
    return render_template("personas/index.html",personas=personas)

@app.route("/personas/create")
def create():
    return render_template('personas/create.html')

@app.route("/personas/create/guardar",methods=['POST'])
def personas_guardar():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    fecha_nacim = request.form['fecha_nac']
    
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO personas (nombre,telefono,fecha_nac) VALUES (?,?,?)",(nombre,telefono,fecha_nacim)
    )
    conn.commit()
    conn.close()
    return redirect('/personas')

@app.route("/personas/edit/<int:id>")
def persona_edit(id):
    conn = sqlite3.connect("kardex.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas WHERE id =?",(id,))
    persona = cursor.fetchone()
    conn.close()
    return render_template("personas/edit.html",persona=persona)

@app.route("/personas/update",methods=['POST'])
def personas_update():
    id = request.form['id']
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    fecha_nac = request.form['fecha_nac']
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE personas SET nombre=?,telefono=?,fecha_nac=? WHERE id=?",(nombre,telefono,fecha_nac,id))
    conn.commit()
    conn.close()
    return redirect("/personas")

@app.route("/personas/delete/<int:id>")
def personas_delete(id):
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personas WHERE id=?",(id))
    conn.commit()
    conn.close()
    return redirect('personas')

if __name__ == "__main__":
    app.run(debug=True)