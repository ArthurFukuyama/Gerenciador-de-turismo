from flask import redirect, url_for


class AuthWsgiMiddleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "")

        # Permite acesso às rotas de login, cadastro e arquivos estáticos sem autenticação
        if path.startswith("/login") or path.startswith("/register") or path.startswith("/static"):
            return self.app(environ, start_response)

        cookie = environ.get("HTTP_COOKIE", "")
        if "session=" not in cookie:
            start_response("302 Found", [("Location", "/login"), ("Content-Type", "text/plain")])
            return [b"Redirecionando para o login..."]

        return self.app(environ, start_response)