from app.models import autenticar_usuario
from flask import Blueprint, redirect, render_template, request, session, url_for

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
  # Se o usuário já estiver logado, redireciona ele para a página principal
  if "user" in session:
    return redirect(url_for("main.welcome"))

  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")

    user = autenticar_usuario(username, password)
    if user:
      session["user"] = user["username"]
      session["nome"] = user["nome"]
      return redirect(url_for("main.welcome"))
    else:
      return render_template(
          "login.html", erro="Usuário ou senha inválidos!"
      )

  return render_template("login.html")


@auth_bp.route("/logout")
def logout():
  session.clear()
  return redirect(url_for("auth.login"))