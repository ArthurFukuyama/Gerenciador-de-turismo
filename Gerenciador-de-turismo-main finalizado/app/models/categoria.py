from app.db import DatabaseConnection

class Categoria:
    def __init__(self, nome: str, usuario_id: int, id: int = None):
        self.id = id
        self.nome = nome
        self.usuario_id = usuario_id

    @classmethod
    def rec_linhas(cls, row):
        if row is None:
            return None
        return cls(id=row['id'], nome=row['nome'], usuario_id=row['usuario_id'])

    def salvar(self):
        with DatabaseConnection() as db:
            sql = "INSERT INTO categorias (nome, usuario_id) VALUES (?, ?)"
            db.cursor.execute(sql, (self.nome, self.usuario_id))
            self.id = db.cursor.lastrowid
        return self

    @classmethod
    def get_por_usuario(cls, usuario_id: int):
        with DatabaseConnection() as db:
            sql = "SELECT id, nome, usuario_id FROM categorias WHERE usuario_id = ?"
            db.cursor.execute(sql, (usuario_id,))
            return [cls.rec_linhas(row) for row in db.cursor.fetchall()]

    @classmethod
    def excluir(cls, categoria_id: int, usuario_id: int):
        with DatabaseConnection() as db:
            sql = "DELETE FROM categorias WHERE id = ? AND usuario_id = ?"
            db.cursor.execute(sql, (categoria_id, usuario_id))