from app.controller import auth_bp, main_bp
from app.middleware import AuthWsgiMiddleware
from flask import Flask


def create_app():
  app = Flask(__name__, template_folder="view")
  app.secret_key = "sua_chave_secreta_super_segura"

  # Envolve a aplicação Flask com o WSGI Middleware
  app.wsgi_app = AuthWsgiMiddleware(app.wsgi_app)

  # Registra os Blueprints
  app.register_blueprint(auth_bp)
  app.register_blueprint(main_bp)

  return app