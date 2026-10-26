from flask import Blueprint, render_template, session, redirect, url_for, request
from app.models.turismo import Places

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def welcome():
    nome_usuario = session.get("nome", "Visitante")
    return render_template("welcome.html", nome=nome_usuario)

@main_bp.route('/ListaLugares', methods=['GET'])
def ListaLugares():
    # Obtém o ID do usuário que está logado na sessão
    user_id = session.get('user_id')
    
    # Se o usuário não estiver logado, redireciona para a tela de login
    if not user_id:
        return redirect(url_for('auth.login'))

    # Busca no banco APENAS os registros pertencentes a este user_id
    lugares_do_usuario = Places.get_lugares_por_usuario(user_id)
    return render_template('lista.html', lugares=lugares_do_usuario)

@main_bp.route('/cadastrar_lugar', methods=['GET', 'POST'])
def cadastrar_lugar():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        lugar = request.form.get('lugar')
        monumento = request.form.get('monumento')

        if not lugar or not monumento:
            return render_template('cadastrar_lugar.html', erro="Preencha todos os campos!")

        # Grava o novo local usando o user_id da sessão ativa
        novo_lugar = Places(lugar=lugar, monumento=monumento, usuario_id=user_id)
        novo_lugar.salvar()

        return redirect(url_for('main.ListaLugares'))

    return render_template('cadastrar_lugar.html')