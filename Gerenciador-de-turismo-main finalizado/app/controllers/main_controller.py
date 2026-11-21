from flask import Blueprint, render_template, redirect, url_for, request, flash, g, make_response, current_app
from app.models.turismo import Places
from app.models.categoria import Categoria
from app.middleware.auth_middlewares import login_required

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@login_required
def welcome():
    return render_template("welcome.html")

@main_bp.route('/mudar_tema/<string:tema>')
def mudar_tema(tema):
    resp = make_response(redirect(request.referrer or url_for('main.welcome')))
    resp.set_cookie('tema', tema, max_age=30*24*60*60)
    flash(f"Tema alterado para {tema}!", "info")
    return resp

@main_bp.route('/ListaLugares')
@login_required
def ListaLugares():
    busca = request.args.get('busca', '').strip()
    lugares = Places.get_lugares_por_usuario(g.usuario.id, busca=busca)
    return render_template('lista.html', lugares=lugares, busca=busca)

@main_bp.route('/cadastrar_lugar', methods=['GET', 'POST'])
@login_required
def cadastrar_lugar():
    if request.method == 'POST':
        lugar = request.form.get('lugar')
        monumento = request.form.get('monumento')
        data_visita = request.form.get('data_visita')
        categoria_id = request.form.get('categoria_id')

        if not lugar or not monumento or not data_visita:
            flash("Preencha todos os campos obrigatórios!", "danger")
            return redirect(url_for('main.cadastrar_lugar'))

        cat_id = int(categoria_id) if categoria_id else None
        novo_lugar = Places(
            lugar=lugar,
            monumento=monumento,
            data_visita=data_visita,
            categoria_id=cat_id,
            usuario_id=g.usuario.id
        )
        novo_lugar.salvar()
        
        current_app.logger.info(f"Usuário {g.usuario.username} cadastrou lugar: {lugar}")
        flash("Ponto turístico salvo com sucesso!", "success")
        return redirect(url_for('main.ListaLugares'))

    categorias = Categoria.get_por_usuario(g.usuario.id)
    return render_template('cadastrar_lugar.html', categorias=categorias)

@main_bp.route('/lugar/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_lugar(id):
    lugar_obj = Places.buscar_por_id(id, g.usuario.id)
    if not lugar_obj:
        flash("Lugar não encontrado ou acesso negado.", "danger")
        return redirect(url_for('main.ListaLugares'))

    if request.method == 'POST':
        lugar = request.form.get('lugar')
        monumento = request.form.get('monumento')
        data_visita = request.form.get('data_visita')
        categoria_id = request.form.get('categoria_id')

        if not lugar or not monumento or not data_visita:
            flash("Preencha todos os campos obrigatórios!", "danger")
            return redirect(url_for('main.editar_lugar', id=id))

        lugar_obj.lugar = lugar
        lugar_obj.monumento = monumento
        lugar_obj.data_visita = data_visita
        lugar_obj.categoria_id = int(categoria_id) if categoria_id else None
        lugar_obj.atualizar()

        current_app.logger.info(f"Usuário {g.usuario.username} editou o lugar ID {id}")
        flash("Ponto turístico atualizado com sucesso!", "success")
        return redirect(url_for('main.ListaLugares'))

    categorias = Categoria.get_por_usuario(g.usuario.id)
    return render_template('editar_lugar.html', lugar=lugar_obj, categorias=categorias)

@main_bp.route('/lugar/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_lugar(id):
    Places.excluir(id, g.usuario.id)
    current_app.logger.info(f"Usuário {g.usuario.username} excluiu o lugar ID {id}")
    flash("Local removido com sucesso!", "success")
    return redirect(url_for('main.ListaLugares'))

@main_bp.route('/categorias', methods=['GET', 'POST'])
@login_required
def gerenciar_categorias():
    if request.method == 'POST':
        nome = request.form.get('nome')
        if not nome:
            flash("O nome da categoria é obrigatório!", "danger")
        else:
            nova_cat = Categoria(nome=nome, usuario_id=g.usuario.id)
            nova_cat.salvar()
            flash("Categoria criada com sucesso!", "success")
        return redirect(url_for('main.gerenciar_categorias'))

    categorias = Categoria.get_por_usuario(g.usuario.id)
    return render_template('categoria.html', categorias=categorias)

@main_bp.route('/categoria/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_categoria(id):
    Categoria.excluir(id, g.usuario.id)
    flash("Categoria removida com sucesso!", "success")
    return redirect(url_for('main.gerenciar_categorias'))