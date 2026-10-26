from app.database import DatabaseConnection
from werkzeug.security import generate_password_hash

def init_usuarios():
    """Cria a tabela de usuários e insere os registros padrão."""
    with DatabaseConnection() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                nome TEXT NOT NULL
            );
        """)

        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
            sql_insert = """
                INSERT INTO usuarios (username, password_hash, nome) 
                VALUES (?, ?, ?)
            """
            users_to_seed = [
                ("admin", generate_password_hash("123"), "Administrador"),
                ("viajante", generate_password_hash("abc"), "Turista Explorador")
            ]
            cursor.executemany(sql_insert, users_to_seed)


def init_turismo():
    """Cria a tabela turismo associada ao ID do usuário."""
    with DatabaseConnection() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS turismo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lugar TEXT NOT NULL,
                monumento TEXT NOT NULL,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            );
        """)

def setup_database():
    """Função principal que orquestra a inicialização de todo o banco de dados."""
    init_usuarios()
    init_turismo()