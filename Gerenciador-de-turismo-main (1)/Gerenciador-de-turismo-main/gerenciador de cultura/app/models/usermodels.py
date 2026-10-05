from werkzeug.security import check_password_hash
from app.database import get_raw_connection

def buscar_usuario_por_username(username: str):
    """Busca o usuário no banco via Cursor e SQL puro com parâmetro seguro."""
    conn = get_raw_connection()
    cursor = conn.cursor()

    try:
        # O caractere '?' garante proteção total contra SQL Injection.
        # Os parâmetros DEVEM ser passados como uma tupla: (username,)
        sql = "SELECT id, username, password_hash, nome FROM usuarios WHERE username = ?"
        cursor.execute(sql, (username,))
        
        row = cursor.fetchone() # Retorna a primeira linha como uma tupla
        
        if row:
            # Mapeia a tupla retornada para um dicionário
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

def autenticar_usuario(username: str, password: str):
    """Autentica o usuário validando a busca via Cursor e a senha com hash."""
    user = buscar_usuario_por_username(username)
    
    if user and check_password_hash(user['password_hash'], password):
        return user
        
    return None