from app.db import DatabaseConnection

class Places:
    def __init__(self, lugar: str, monumento: str, data_visita: str, usuario_id: int, categoria_id: int = None, id: int = None, categoria_nome: str = None):
        self.id = id
        self.lugar = lugar
        self.monumento = monumento
        self.data_visita = data_visita
        self.categoria_id = categoria_id
        self.usuario_id = usuario_id
        self.categoria_nome = categoria_nome

    @classmethod
    def rec_linhas(cls, row):
        if row is None:
            return None
        return cls(
            id=row['id'],
            lugar=row['lugar'],
            monumento=row['monumento'],
            data_visita=row['data_visita'],
            categoria_id=row['categoria_id'],
            usuario_id=row['usuario_id'],
            categoria_nome=row['categoria_nome'] if 'categoria_nome' in row.keys() else None
        )

    def salvar(self):
        with DatabaseConnection() as db:
            sql = "INSERT INTO turismo (lugar, monumento, data_visita, categoria_id, usuario_id) VALUES (?, ?, ?, ?, ?)"
            db.cursor.execute(sql, (self.lugar, self.monumento, self.data_visita, self.categoria_id, self.usuario_id))
            self.id = db.cursor.lastrowid
        return self

    def atualizar(self):
        """Atualiza os dados de um lugar existente pertencente ao usuário."""
        with DatabaseConnection() as db:
            sql = """
                UPDATE turismo
                SET lugar = ?, monumento = ?, data_visita = ?, categoria_id = ?
                WHERE id = ? AND usuario_id = ?
            """
            db.cursor.execute(sql, (self.lugar, self.monumento, self.data_visita, self.categoria_id, self.id, self.usuario_id))
        return self

    @classmethod
    def buscar_por_id(cls, lugar_id: int, usuario_id: int):
        """Busca um lugar específico garantindo que pertence ao usuário logado."""
        with DatabaseConnection() as db:
            sql = """
                SELECT t.id, t.lugar, t.monumento, t.data_visita, t.categoria_id, t.usuario_id, c.nome as categoria_nome
                FROM turismo t
                LEFT JOIN categorias c ON t.categoria_id = c.id
                WHERE t.id = ? AND t.usuario_id = ?
            """
            db.cursor.execute(sql, (lugar_id, usuario_id))
            return cls.rec_linhas(db.cursor.fetchone())

    @classmethod
    def get_lugares_por_usuario(cls, usuario_id: int, busca: str = ""):
        """Lista os lugares do usuário com filtro opcional por lugar ou monumento."""
        with DatabaseConnection() as db:
            if busca:
                termo = f"%{busca}%"
                sql = """
                    SELECT t.id, t.lugar, t.monumento, t.data_visita, t.categoria_id, t.usuario_id, c.nome as categoria_nome
                    FROM turismo t
                    LEFT JOIN categorias c ON t.categoria_id = c.id
                    WHERE t.usuario_id = ? AND (t.lugar LIKE ? OR t.monumento LIKE ?)
                    ORDER BY t.data_visita DESC
                """
                db.cursor.execute(sql, (usuario_id, termo, termo))
            else:
                sql = """
                    SELECT t.id, t.lugar, t.monumento, t.data_visita, t.categoria_id, t.usuario_id, c.nome as categoria_nome
                    FROM turismo t
                    LEFT JOIN categorias c ON t.categoria_id = c.id
                    WHERE t.usuario_id = ?
                    ORDER BY t.data_visita DESC
                """
                db.cursor.execute(sql, (usuario_id,))
            return [cls.rec_linhas(row) for row in db.cursor.fetchall()]

    @classmethod
    def excluir(cls, lugar_id: int, usuario_id: int):
        with DatabaseConnection() as db:
            sql = "DELETE FROM turismo WHERE id = ? AND usuario_id = ?"
            db.cursor.execute(sql, (lugar_id, usuario_id))