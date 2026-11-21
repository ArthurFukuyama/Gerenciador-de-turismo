from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app.models.usermodels import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if "user_id" in session:
        return redirect(url_for('main.welcome'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.autenticar(username, password)
        if user:
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            session['nome'] = user.nome
            current_app.logger.info(f"Login efetuado: {username}")
            flash("Login efetuado com sucesso!", "success")
            return redirect(url_for('main.welcome'))
            
        current_app.logger.warning(f"Falha de login: {username}")
        flash("Usuário ou senha inválidos!", "danger")
        return render_template('login.html')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if "user_id" in session:
        return redirect(url_for('main.welcome'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        username = request.form.get('username')
        password = request.form.get('password')

        if not nome or not username or not password:
            flash("Preencha todos os campos obrigatórios!", "danger")
            return render_template('register.html')

        if User.buscar_por_username(username):
            flash("Nome de usuário já está em uso.", "danger")
            return render_template('register.html')

        novo_usuario = User(username=username, nome=nome)
        novo_usuario.set_password(password)
        novo_usuario.salvar()
        
        flash("Cadastro realizado com sucesso! Faça login abaixo.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Sessão encerrada.", "info")
    return redirect(url_for('auth.login'))