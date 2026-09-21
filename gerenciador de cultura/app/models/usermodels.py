USUARIOS_TESTE = [
    {"username": "admin", "password": "123", "nome": "Administrador"},
    {"username": "viajante", "password": "abc", "nome": "Turista Explorador"},
]


def autenticar_usuario(username, password):
  for user in USUARIOS_TESTE:
    if user["username"] == username and user["password"] == password:
      return user
  return None