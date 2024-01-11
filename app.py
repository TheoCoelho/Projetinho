"""from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# Configuração do banco de dados MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'projetinho'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['username']
        email = request.form['email']
        senha = request.form['password']
        datanasc = request.form['dob']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO login (Nome, email, senha, datanasc) VALUES (%s, %s, %s, %s)",
                    (nome, email, senha, datanasc))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/login', methods=['POST',"GET"])
def login():
    email = request.form['email']
    senha = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM login WHERE email = %s AND senha = %s", (email, senha))
    user = cur.fetchone()
    cur.close()

    if user:
        # Autenticação bem-sucedida, redirecionar para a página desejada após o login
        return "Login bem-sucedido"
    else:
        # Autenticação falhou, redirecionar para a página de login
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)"""


from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configurações do banco de dados MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'projetinho'

mysql = MySQL(app)

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        datanasc = request.form['datanasc']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM login WHERE email = %s', (email,))
        user = cur.fetchone()

        if user:
            return 'E-mail já cadastrado!'

        cur.execute('INSERT INTO login (Nome, email, senha, datanasc) VALUES (%s, %s, %s, %s)', (nome, email, senha, datanasc))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))

    return render_template('cadastro.html')

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE email = %s AND senha = %s', (email, senha))
        user = cur.fetchone()
        cur.close()

        if user:
            session['email'] = email
            return redirect(url_for('perfil'))

        return 'Credenciais inválidas!'

    return render_template('login.html')

# Página do perfil
@app.route('/perfil')
def perfil():
    if 'email' in session:
        email = session['email']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        user = cur.fetchone()
        cur.close()

        return render_template('perfil.html', user=user)

    return redirect(url_for('login'))

# Logout
"""@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))"""

if __name__ == '__main__':
    app.run(debug=True)