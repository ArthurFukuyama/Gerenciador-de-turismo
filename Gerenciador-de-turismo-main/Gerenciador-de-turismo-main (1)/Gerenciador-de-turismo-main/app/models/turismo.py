from app.database import DatabaseConnection

class Places:
    def __init__(self, lugar: str, monumento: str, id: int = None):
        self.id = id
        self.lugar = lugar
        self.monumento = monumento

    @classmethod
    def rec_linhas(cls,row):
        if row is None:
            return None
        return cls(
            id = row['id'],
            lugar = row['lugar'],
            monumento = row['monumento'],
        )
    
    def get_lugares(cls, id):
       with DatabaseConnection() as cursor:
            sql = "SELECT id, lugar,monumento FROM usuarios WHERE id = ?"
            cursor.execute(sql, (id,))
            row = cursor.fetchall()
            listaLugares = []
            for l in row:
                listaLugares.append(cls.rec_linhas(l))
            return listaLugares