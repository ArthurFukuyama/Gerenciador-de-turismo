from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash

# Engine configurado para SQLite
engine = create_engine('sqlite:///app.db', echo=False)

def get_raw_connection():
    """Retorna uma conexão bruta de baixo nível (DBAPI / sqlite3)."""
    return engine.raw_connection()

def init_db():
    """Cria a tabela e insere os dados iniciais usando Cursor e SQL puro."""
    conn = get_raw_connection()
    cursor = conn.cursor()

    try:
        # 1. Criação da tabela
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                nome TEXT NOT NULL
            );
        """)

        # 2. Verifica se a tabela está vazia
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        count = cursor.fetchone()[0]

        if count == 0:
            # 3. Inserção protegida contra SQL Injection com placeholders '?'
            sql_insert = """
                INSERT INTO usuarios (username, password_hash, nome) 
                VALUES (?, ?, ?)
            """
            
            users_to_seed = [
                ("admin", generate_password_hash("123"), "Administrador"),
                ("viajante", generate_password_hash("abc"), "Turista Explorador")
            ]

            # executemany aplica os parâmetros com segurança para cada item da lista
            cursor.executemany(sql_insert, users_to_seed)
            conn.commit()  # Confirma as alterações no banco

    finally:
        # Garante que o cursor e a conexão sejam fechados
        cursor.close()
        conn.close()