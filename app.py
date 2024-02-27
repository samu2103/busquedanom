from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import re

app = Flask(__name__)
app.secret_key = 'upchiapitos'  # Clave secreta para la sesión

datos = pd.read_excel("datospersonales.xlsx")

def search_nombres(nombres):
    nombres_lista = [nombre.strip() for nombre in nombres.split(',')]
    
    coincidencias = []
    for nombre in nombres_lista:
        datos[['Clave', 'Nombre', 'Correo', 'Telefono']] = datos[['Clave', 'Nombre', 'Correo', 'Telefono']].fillna('')
        coincidence = datos[datos['Nombre'].str.contains(nombre, flags=re.IGNORECASE, regex=True)]
        coincidencias.extend(coincidence[['Clave', 'Nombre', 'Correo', 'Telefono']].to_dict(orient='records'))
    
    return coincidencias

def verificar_credenciales(usuario, contrasena):
    return usuario == 'samuel' and contrasena == 'saeh'

@app.route('/')
def index():
    if 'usuario' in session:
        return render_template('Formulario.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        if verificar_credenciales(usuario, contrasena):
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            return render_template('login.html', mensaje='Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/Lista', methods=['POST'])
def lista():
    search_nombres_input = request.form['nombre']
    resultados = search_nombres(search_nombres_input)
    return render_template('Formulario.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
