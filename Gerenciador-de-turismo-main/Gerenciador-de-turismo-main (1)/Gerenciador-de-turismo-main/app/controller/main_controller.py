from flask import Blueprint, render_template, session, redirect, url_for
from app.models.turismo import Places
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def welcome():
  nome_usuario = session.get("nome", "Visitante")
  return render_template("welcome.html", nome=nome_usuario)

@main_bp.route('/ListaLugares', methods = ['GET'])
def ListaLugares(id):
    ln = Places.get_lugares(id)
    return render_template( 'lista.html', lugares = ln)

@main_bp.route('/Paralistas')
def mandar():
    return redirect(url_for('main.ListaLugares'))