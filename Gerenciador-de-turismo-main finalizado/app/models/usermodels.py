from werkzeug.security import generate_password_hash, check_password_hash
from app.db import DatabaseConnection

class User:
    def __init__(self, username: str, nome: str, password_hash: str = None, id: int = None):
        self.id = id
        self.username = username
        self.nome = nome
        self.password_hash = password_hash

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def salvar(self):
        with DatabaseConnection() as db:
            if self.id is None:
                sql = "INSERT INTO usuarios (username, password_hash, nome) VALUES (?, ?, ?)"
                db.cursor.execute(sql, (self.username, self.password_hash, self.nome))
                self.id = db.cursor.lastrowid
            else:
                sql = "UPDATE usuarios SET username = ?, password_hash = ?, nome = ? WHERE id = ?"
                db.cursor.execute(sql, (self.username, self.password_hash, self.nome, self.id))
        return self

    @classmethod
    def buscar_por_username(cls, username: str):
        sql = "SELECT id, username, password_hash, nome FROM usuarios WHERE username = ?"
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (username,))
            row = db.cursor.fetchone()
            if row:
                return cls(id=row['id'], username=row['username'], password_hash=row['password_hash'], nome=row['nome'])
        return None

    @classmethod
    def buscar_por_id(cls, user_id: int):
        sql = "SELECT id, username, password_hash, nome FROM usuarios WHERE id = ?"
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (user_id,))
            row = db.cursor.fetchone()
            if row:
                return cls(id=row['id'], username=row['username'], password_hash=row['password_hash'], nome=row['nome'])
        return None

    @classmethod
    def autenticar(cls, username: str, password: str):
        user = cls.buscar_por_username(username)
        if user and user.check_password(password):
            return user
        return None