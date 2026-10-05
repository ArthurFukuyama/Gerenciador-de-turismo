from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import autenticar_usuario, cadastrar_usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if "user" in session:
        return redirect(url_for('main.welcome'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = autenticar_usuario(username, password)
        if user:
            session['user'] = user['username']
            session['nome'] = user['nome']
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

        sucesso, mensagem = cadastrar_usuario(username, password, nome)
        if sucesso:
            # Redireciona para o login exibindo uma mensagem positiva
            return render_template('login.html', mensagem="Cadastro realizado com sucesso! Faça login abaixo.")
        else:
            return render_template('register.html', erro=mensagem)

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))