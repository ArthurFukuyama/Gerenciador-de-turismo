from app.db import DatabaseConnection, DB_PATH
from app.models.usermodels import User
from app.models.categoria import Categoria
from app.models.turismo import Places

def iniciar_banco():
    with DatabaseConnection() as db:
        db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                nome TEXT NOT NULL
            );
        """)
        
        db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
            );
        """)

        db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS turismo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lugar TEXT NOT NULL,
                monumento TEXT NOT NULL,
                data_visita TEXT NOT NULL,
                categoria_id INTEGER,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id) ON DELETE SET NULL
            );
        """)

    # Só insere os dados iniciais na primeira vez (quando o admin ainda não existe)
    if not User.buscar_por_username("admin"):
        admin = User(username="admin", nome="Administrador")
        admin.set_password("123")
        admin.salvar()

        # Criação de múltiplas categorias iniciais via Model
        nomes_categorias = [
            "Parque / Natureza",
            "Museus e Cultura",
            "Praias e Litoral",
            "Monumentos Históricos",
            "Gastronomia"
        ]
        
        categorias_criadas = []
        for nome in nomes_categorias:
            cat = Categoria(nome=nome, usuario_id=admin.id)
            cat.salvar()
            categorias_criadas.append(cat)

        # Exemplo de lugar inicial associado à primeira categoria ("Parque / Natureza")
        lugar = Places(
            lugar="Rio de Janeiro",
            monumento="Cristo Redentor",
            data_visita="2026-05-10",
            categoria_id=categorias_criadas[0].id,
            usuario_id=admin.id
        )
        lugar.salvar()

if __name__ == '__main__':
    iniciar_banco()
    print(f"Banco inicializado em: {DB_PATH}")