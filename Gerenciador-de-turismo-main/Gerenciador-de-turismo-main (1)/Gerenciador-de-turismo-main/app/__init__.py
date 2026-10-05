from flask import Flask
from app.init_db import setup_database
from app.controller import auth_bp, main_bp
from app.middleware import AuthWsgiMiddleware

def create_app():
    app = Flask(__name__, template_folder='view')
    app.secret_key = "sua_chave_secreta_super_segura"

    # Executa a inicialização do banco de dados uma vez antes de tudo
    setup_database()

    # Registra o Middleware WSGI
    app.wsgi_app = AuthWsgiMiddleware(app.wsgi_app)

    # Registra os Blueprints (Controllers)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app