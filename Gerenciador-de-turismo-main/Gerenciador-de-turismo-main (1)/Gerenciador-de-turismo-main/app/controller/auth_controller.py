from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if "user" in session:
        return redirect(url_for('main.welcome'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Uso do método de classe para autenticar
        user = User.autenticar(username, password)
        if user:
            session['user'] = user.username
            session['nome'] = user.nome
            return redirect(url_for('main.welcome'))
            
        return render_template('login.html', erro="Usuário ou senha inválidos!")

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if "user" in session:
        return redirect(url_for('main.welcome'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        username = request.form.get('username')
        password = request.form.get('password')

        if not nome or not username or not password:
            return render_template('register.html', erro="Preencha todos os campos!")

        # Verifica se o usuário já existe no banco
        if User.buscar_por_username(username):
            return render_template('register.html', erro="Nome de usuário já está em uso.")

        try:
            # Instancia o novo usuário, define a senha e salva
            novo_usuario = User(username=username, nome=nome)
            novo_usuario.set_password(password)
            novo_usuario.salvar()

            return render_template('login.html', mensagem="Cadastro realizado com sucesso! Faça login abaixo.")
        except Exception as e:
            return render_template('register.html', erro=f"Erro ao salvar cadastro: {str(e)}")

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

