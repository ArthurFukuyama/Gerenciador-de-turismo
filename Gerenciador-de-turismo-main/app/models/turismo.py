from app.database import DatabaseConnection

class Places:
    def __init__(self, lugar: str, monumento: str, usuario_id: int, id: int = None):
        self.id = id
        self.lugar = lugar
        self.monumento = monumento
        self.usuario_id = usuario_id

    @classmethod
    def rec_linhas(cls, row):
        if row is None:
            return None
        return cls(
            id=row['id'],
            lugar=row['lugar'],
            monumento=row['monumento'],
            usuario_id=row['usuario_id']
        )

    def salvar(self):
        """Salva o lugar vinculando ao usuario_id."""
        with DatabaseConnection() as cursor:
            sql = """
                INSERT INTO turismo (lugar, monumento, usuario_id)
                VALUES (?, ?, ?)
            """
            cursor.execute(sql, (self.lugar, self.monumento, self.usuario_id))
            self.id = cursor.lastrowid
        return self

    @classmethod
    def get_lugares_por_usuario(cls, usuario_id: int):
        """Retorna ESTRITAMENTE os lugares cadastrados pelo usuário fornecido."""
        with DatabaseConnection() as cursor:
            sql = "SELECT id, lugar, monumento, usuario_id FROM turismo WHERE usuario_id = ?"
            cursor.execute(sql, (usuario_id,))
            rows = cursor.fetchall()
            return [cls.rec_linhas(row) for row in rows]