from functools import wraps
from flask import session, redirect, url_for, g
from app.models.usermodels import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('auth.login'))
        
        usuario = User.buscar_por_id(user_id)
        if not usuario:
            session.clear()
            return redirect(url_for('auth.login'))
            
        g.usuario = usuario
        return f(*args, **kwargs)
    return decorated_function