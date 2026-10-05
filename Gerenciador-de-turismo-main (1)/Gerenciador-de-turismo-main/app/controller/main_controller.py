from flask import Blueprint, render_template, session

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def welcome():
  nome_usuario = session.get("nome", "Visitante")
  return render_template("welcome.html", nome=nome_usuario)