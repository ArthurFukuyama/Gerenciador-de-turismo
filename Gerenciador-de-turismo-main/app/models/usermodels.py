from werkzeug.security import generate_password_hash, check_password_hash
from app.database import DatabaseConnection

class User:
    def __init__(self, username: str, nome: str, password_hash: str = None, id: int = None):
        self.id = id
        self.username = username
        self.nome = nome
        self.password_hash = password_hash

    def set_password(self, password: str):
        """Gera e atribui o hash seguro para a senha recebida."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifica se a senha informada bate com o hash armazenado."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def salvar(self):
        """
        Insere um novo usuário ou atualiza um existente no banco de dados
        usando a conexão gerenciada por contexto com 'with'.
        """
        with DatabaseConnection() as cursor:
            if self.id is None:
                # Inserção de novo usuário
                sql = """
                    INSERT INTO usuarios (username, password_hash, nome)
                    VALUES (?, ?, ?)
                """
                cursor.execute(sql, (self.username, self.password_hash, self.nome))
                self.id = cursor.lastrowid
            else:
                # Atualização de usuário existente
                sql = """
                    UPDATE usuarios
                    SET username = ?, password_hash = ?, nome = ?
                    WHERE id = ?
                """
                cursor.execute(sql, (self.username, self.password_hash, self.nome, self.id))
        return self

    @classmethod
    def buscar_por_username(cls, username: str):
        """Método de classe para buscar um usuário pelo username no banco."""
        sql = "SELECT id, username, password_hash, nome FROM usuarios WHERE username = ?"
        with DatabaseConnection() as cursor:
            cursor.execute(sql, (username,))
            row = cursor.fetchone()
            if row:
                return cls(
                    id=row['id'],
                    username=row['username'],
                    password_hash=row['password_hash'],
                    nome=row['nome']
                )
        return None

    @classmethod
    def buscar_por_id(cls, user_id: int):
        """Método de classe para buscar um usuário por ID."""
        sql = "SELECT id, username, password_hash, nome FROM usuarios WHERE id = ?"
        with DatabaseConnection() as cursor:
            cursor.execute(sql, (user_id,))
            row = cursor.fetchone()
            if row:
                return cls(
                    id=row['id'],
                    username=row['username'],
                    password_hash=row['password_hash'],
                    nome=row['nome']
                )
        return None

    @classmethod
    def autenticar(cls, username: str, password: str):
        """Método de classe que valida o login de um usuário."""
        user = cls.buscar_por_username(username)
        if user and user.check_password(password):
            return user
        return None