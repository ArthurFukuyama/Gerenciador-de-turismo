from werkzeug.security import check_password_hash, generate_password_hash
from app.database import get_raw_connection

def buscar_usuario_por_username(username: str):
    """Busca o usuário no banco via Cursor e SQL puro com parâmetro seguro."""
    conn = get_raw_connection()
    cursor = conn.cursor()

    try:
        sql = "SELECT id, username, password_hash, nome FROM usuarios WHERE username = ?"
        cursor.execute(sql, (username,))
        row = cursor.fetchone()
        
        if row:
            return {
                "id": row[0],
                "username": row[1],
                "password_hash": row[2],
                "nome": row[3]
            }
        return None
    finally:
        cursor.close()
        conn.close()

def cadastrar_usuario(username: str, password: str, nome: str):
    """
    Insere um novo usuário no banco usando Cursor e SQL parametrizado (?).
    Retorna True se cadastrado com sucesso ou False se o username já existir.
    """
    # 1. Verifica se já existe um usuário com o mesmo username
    if buscar_usuario_por_username(username):
        return False, "Nome de usuário já está em uso."

    # 2. Gera o hash seguro da senha
    password_hash = generate_password_hash(password)

    conn = get_raw_connection()
    cursor = conn.conn.cursor() if hasattr(conn, 'conn') else conn.cursor()

    try:
        sql = """
            INSERT INTO usuarios (username, password_hash, nome) 
            VALUES (?, ?, ?)
        """
        # A instrução e os parâmetros em tupla evitam SQL Injection
        cursor.execute(sql, (username, password_hash, nome))
        conn.commit()  # Confirma a gravação no banco de dados
        return True, "Usuário cadastrado com sucesso!"
    except Exception as e:
        conn.rollback()
        return False, f"Erro ao cadastrar no banco: {str(e)}"
    finally:
        cursor.close()
        conn.close()

def autenticar_usuario(username: str, password: str):
    """Autentica o usuário validando a busca via Cursor e a senha com hash."""
    user = buscar_usuario_por_username(username)
    
    if user and check_password_hash(user['password_hash'], password):
        return user
        
    return None