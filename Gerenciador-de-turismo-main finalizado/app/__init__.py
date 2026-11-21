import os
from flask import Flask, render_template
from iniciar_db import iniciar_banco

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    root_dir = os.path.dirname(base_dir)
    
    template_dir = os.path.join(base_dir, 'view')
    static_dir = os.path.join(root_dir, 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.secret_key = 'sua_chave_secreta_aqui'

    # Garante que o banco e as tabelas sejam criados na 1ª execução

    iniciar_banco()

    from app.controllers.auth_controller import auth_bp
    from app.controllers.main_controller import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.warning(f"Rota não encontrada: {e}")
        return render_template('404.html'), 404

    return app