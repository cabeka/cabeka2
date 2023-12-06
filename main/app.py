from flask import Flask, request, redirect, render_template, url_for, session
import mysql.connector
import os

conexao = mysql.connector.connect(
    host="roundhouse.proxy.rlwy.net",
    user="root",
    password="bC2A4Gf1A3A3e3BCD2Efe65BadE5ehHb",
    database="railway",
    port="44601",
)

app = Flask(__name__, template_folder='../templates')
app.secret_key = 'super secret key'

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':        
        nome = request.form['nome']
        senha = request.form['senha']
        if not nome or not senha:
            msg = 'Nome/senha em branco.'
        else:
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, senha FROM pessoas WHERE nome = %s AND senha = %s", (nome, senha))
            autent = cursor.fetchone()
            cursor.close()
            conexao.commit()
            if autent:
                session['logado'] = True
                session['nome'] = autent[0]
                return redirect(url_for('home'))
            else:
                msg = 'Nome/senha inválido.'
    return render_template('index.html', msg=msg)

@app.route('/home')
def home():
    if 'logado' in session and session['logado']:
        senha = request.args.get('senha')
        cursor = conexao.cursor()
        cursor.execute("SELECT nome FROM pessoas WHERE senha = %s", (senha,))
        jogador = cursor.fetchone()
        cursor.close()
        return render_template('home.html', jogador=jogador)
    else:
        return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    msg = ''
    if request.method == 'POST':
        nome = request.form['nome'].capitalize()
        senha = request.form['senha']
        if not nome or not senha:
            msg = 'Nome/senha em branco.'
        else:
            cursor = conexao.cursor()
            cursor.execute("SELECT senha FROM pessoas WHERE nome = %s", (nome,))
            conta = cursor.fetchone()
            if conta:
                msg = 'A conta já existe'
            else:
                cursor.execute("INSERT INTO pessoas(nome, senha) VALUES(%s, %s);", (nome, senha))
                cursor.close()
                conexao.commit()
                return redirect(url_for('login'))
    return render_template('cadastro.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('logado', None)
    session.pop('nome', None)
    return redirect(url_for('login'))

@app.route('/abrir_proh')
def abrir_proh():
    pasta_proh = os.path.join(os.getcwd(), 'proh')
    
    if os.path.exists(pasta_proh):
        os.chdir(pasta_proh)
        os.system('python app.py')
        return "Arquivo app.py iniciado com sucesso."
    else:
        return "Pasta 'proh' não encontrada."

if __name__ == '__main__':
    app.run(debug=True)
    conexao.close()
