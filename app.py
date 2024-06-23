from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
import pyodbc
import re

app = Flask(__name__)

server = "127.0.0.1"
database = "meubanco"
database_user = "root"
driver = "MySQL ODBC 8.4 Unicode Driver"
password = ""
app.secret_key = "tititititi"

@app.route('/')
def index():
    conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={database_user};PWD={password}"
    message = get_flashed_messages()
    print(message)
    conn = pyodbc.connect(conn_str)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuario")

    usuarios = cursor.fetchall()

    user = {'username': 'Alice', 'is_authenticated': False}
    return render_template('index.html', usuarios=usuarios, message=message)

@app.route('/page')
def page():
    return render_template('page.html')

def validar_cpf(cpf):
    # Regex para verificar o formato XXX.XXX.XXX-XX
    regex = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
    match = re.match(regex, cpf)
    return bool(match)


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={database_user};PWD={password}"

    if request.method == "POST":
        nome = request.form['nome'].capitalize()
        sobrenome = request.form['sobrenome'].capitalize()
        endereco = request.form['endereco'].capitalize()
        cpf = request.form['cpf']

        if validar_cpf(cpf):
            print('cpf ok!')
        else:
            print('cpf errado!')

        # Remover os caracteres especiais do CPF
        cpf = cpf.replace(".", "").replace("-", "")

        print(cpf)

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO usuario (`nome`, `sobrenome`, `endereco`, `cpf`) VALUES ('{nome}', '{sobrenome}', '{endereco}', '{cpf}');")
        # cursor.execute("INSERT INTO usuario(nome, sobrenome, endereco, cpf) VALUES (?,?,?,?)", nome, sobrenome, endereco, cpf))
        conn.commit()
        flash("usuario adicionado com sucesso!")
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
