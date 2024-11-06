from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('registro.db')
    conn.row_factory = sqlite3.Row
    return conn

# Página principal
@app.route('/')
def index():
    return render_template('manager.html')

# Página para formulario de registro de alumnos
@app.route('/register_alumno')
def register_alumno_form():
    return render_template('register_alumno.html')

# Procesar el registro de alumnos
@app.route('/register_alumno', methods=['POST'])
def register_alumno():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    grado = request.form['grado']
    especialidad = request.form['especialidad']
    username = request.form['username']
    password = request.form['password']

    if not (username and password):
        flash('Nombre de usuario y contraseña son requeridos.')
        return redirect(url_for('register_alumno_form'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            grado TEXT NOT NULL,
            especialidad TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    try:
        cursor.execute('''
            INSERT INTO alumnos (nombre, apellido, grado, especialidad, username, password)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, apellido, grado, especialidad, username, password))
        conn.commit()
        flash('Registro de alumno exitoso!')
    except sqlite3.IntegrityError:
        flash('El nombre de usuario ya existe.')
    finally:
        conn.close()

    return redirect(url_for('register_alumno'))

# Página para formulario de registro de maestros
@app.route('/register_teacher')
def register_teacher_form():
    return render_template('register_teacher.html')

# Procesar el registro de maestros
@app.route('/register_teacher', methods=['POST'])
def register_teacher_submit():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    encargado_de = request.form['encargado_de']
    username = request.form['username']
    password = request.form['password']

    if not (username and password):
        flash('Nombre de usuario y contraseña son requeridos.')
        return redirect(url_for('register_teacher_form'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maestros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            encargado_de TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    try:
        cursor.execute('''
            INSERT INTO maestros (nombre, apellido, encargado_de, username, password)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, apellido, encargado_de, username, password))
        conn.commit()
        flash('Registro de maestro exitoso!')
    except sqlite3.IntegrityError:
        flash('El nombre de usuario ya existe.')
    finally:
        conn.close()

    return redirect(url_for('index'))

# Mostrar lista de alumnos
@app.route('/show_students')
def show_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alumnos')
    alumnos = cursor.fetchall()
    conn.close()
    return render_template('show_students.html', alumnos=alumnos)

# Mostrar lista de maestros
@app.route('/show_teachers')
def show_teachers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM maestros')
    maestros = cursor.fetchall()
    conn.close()
    return render_template('show_teachers.html', maestros=maestros)

# Eliminar alumno
@app.route('/delete_student/<int:id>', methods=['POST'])
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM alumnos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Alumno eliminado con éxito.')
    return redirect(url_for('show_students'))

# Eliminar maestro
@app.route('/delete_teacher/<int:id>', methods=['POST'])
def delete_teacher(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM maestros WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Maestro eliminado con éxito.')
    return redirect(url_for('show_teachers'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)