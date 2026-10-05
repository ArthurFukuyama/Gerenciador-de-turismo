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
    """Cria a tabela de turismo e insere os registros padrão."""
    with DatabaseConnection() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS turismo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lugar TEXT UNIQUE NOT NULL,
                monumento TEXT NOT NULL
            );
        """)

        cursor.execute("SELECT COUNT(*) FROM turismo")
        if cursor.fetchone()[0] == 0:
            # Corrigido para 2 placeholders '?, ?' correspondentes a 'lugar, monumento'
            sql_insert = """
                INSERT INTO turismo (lugar, monumento) 
                VALUES (?, ?)
            """
            turismo_to_seed = [
                ("Rio de Janeiro", "Cristo Redentor"),
                ("São Paulo", "MASP")
            ]
            cursor.executemany(sql_insert, turismo_to_seed)


def setup_database():
    """Função principal que orquestra a inicialização de todo o banco de dados."""
    init_usuarios()
    init_turismo()