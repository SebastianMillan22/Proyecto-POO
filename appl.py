from flask import Flask, render_template, request, session, redirect, url_for
import config
'Modulo DB flask'
from flask_mysqldb import MySQL

'Instanciación de objeto Flask'
app = Flask(__name__) 

'Configuración datos para la DB'
app.config['SECRET_KEY'] = config.HEX_SEC_KEY
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

'Ruta de formulario alojamiento LOGIN '
@app.route('/', methods=['GET'])
def home():
    'Busca el archivo y lo ejecuta '
    return render_template('index.html')


'Ruta de login'
@app.route('/login', methods=['POST'])
def login():
    'Recibiremos email y password'
    email = request.form['email']
    password = request.form['password']
    'Conexión a DB'
    conec = mysql.connection.cursor()
    'Generar consulta en DB'
    conec.execute("SELECT * FROM users WHERE email = %s AND password = %s ", (email, password))
    '¿Ha habido coincidencia?'
    user = conec.fetchone()
    conec.close()
    
    if user is not None:
        session['email'] = email 
        session['name'] = user[1]
        session['surnames'] = user[2]
        
        return redirect(url_for('tasks'))
    else: 
        return render_template('index.html', message="Las credenciales no son correctas")
    
    
@app.route('/tasks', methods=['GET'])
def tasks():
    return render_template('tasks.html')
        

 

if __name__ == '__main__':
    'Ejecutar app en modo desarrollo para cambiar y ejecutar cambios al momento'
    app.run(debug=True)
    