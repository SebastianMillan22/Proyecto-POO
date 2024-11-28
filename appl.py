from flask import Flask, render_template, request, session, redirect, url_for
import config
'Modulo DB flask'
from flask_mysqldb import MySQL
from datetime import datetime

'Instanciación de objeto Flask'
app = Flask(__name__) 

'Configuración datos para la DB'
app.config['SECRET_KEY'] = config.HEX_SEC_KEY  
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

'Ruta de formulario alojamiento LOGIN  '              
@app.route('/', methods=['GET'])
def home():
    'Busca el archivo y lo ejecuta '
    return render_template('index.html')


'Ruta de login'
@app.route('/login', methods=['POST'])
def login():
    'Recibiremos email y password'    
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    'Conexión a DB'
    conec = mysql.connection.cursor()
    'Generar consulta en DB'
    conec.execute("SELECT * FROM users WHERE correo = %s AND contraseña = %s ", (correo, contraseña))
    '¿Ha habido coincidencia?' 
    user = conec.fetchone()
    conec.close()
    
    if user is not None:
        session['correo'] = correo 
        session['nombre'] = user[1]
        session['apellido'] = user[2]
        
        return redirect(url_for('tasks'))
    else: 
        return render_template('index.html', message="Las credenciales no son correctas")
    
    
@app.route('/tasks', methods=['GET'])
def tasks():
    email = session['correo']
    conec = mysql.connection.cursor()
    conec.execute("SELECT * FROM tasks WHERE correo = %s", [email])
    tasks = conec.fetchall()
    
    insertObject = []
    columnNames = [column[0] for column in conec.description]
    for record in tasks:
        insertObject.append(dict(zip(columnNames, record)))
    conec.close()
    return render_template('tasks.html', taks= insertObject)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/new-task', methods=['POST'])
def newTask():
    correo = session['correo']
    titulo = request.form.get('title', '')
    descripcion = request.form.get('descripcion', '')
    d = datetime.now()
    dateTask = d.strftime("%Y-%m-%d $H:%M:%S")
    
    if titulo and descripcion and correo:
        conec = mysql.connection.cursor()
        sql = "INSERT INTO tasks (correo, title, descripcion, fecha_tarea) VALUES (%s, %s, %s, %s)"
        data = (correo, titulo, descripcion, dateTask)
        conec.execute(sql,data)
        mysql.connection.commit()
        
    return redirect(url_for('tasks'))

@app.route('/new-user', methods=['POST'])
def newUser():
    name = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    
    if name and apellido and correo and contraseña: 
        conec = mysql.connection.cursor()
        sql = "INSERT INTO users (nombre, apellido, correo, contraseña) VALUES (%s, %s, %s, %s)"
        data = (name, apellido, correo, contraseña)
        conec.execute(sql, data)
        mysql.connection.commit()
        
    return redirect(url_for('tasks'))

 

if __name__ == '__main__':
    'Ejecutar app en modo desarrollo para cambiar y ejecutar cambios al momento'
    app.run(debug=True)
    