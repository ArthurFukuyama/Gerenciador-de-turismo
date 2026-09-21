from flask import redirect, url_for


class AuthWsgiMiddleware:

  def __init__(self, app):
    self.app = app

  def __call__(self, environ, start_response):
    # O middleware WSGI roda antes do ciclo de requisição do Flask.
    # Podemos inspecionar o caminho da requisição (PATH_INFO) no environ.
    path = environ.get("PATH_INFO", "")

    # Se a rota for de login ou arquivos estáticos, deixa passar
    if path.startswith("/login") or path.startswith("/static"):
      return self.app(environ, start_response)

    # Para verificar a sessão do Flask dentro do WSGI, precisamos avaliar o contexto
    # Ou podemos delegar o redirecionamento se o cookie de sessão não existir ou estiver vazio.
    # Nota: A checagem fina de sessão do Flask pode ser feita verificando os cookies da requisição:
    cookie = environ.get("HTTP_COOKIE", "")
    if "session=" not in cookie:
      # Redireciona para /login via WSGI response (302 Found)
      start_response(
          "302 Found", [("Location", "/login"), ("Content-Type", "text/plain")]
      )
      return [b"Redirecionando para o login..."]

    return self.app(environ, start_response)