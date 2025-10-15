from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.baseDatos import Usuario

# Crear el Blueprint
perfil_usuario_bp = Blueprint('perfil_usuario_bp', __name__, template_folder='../templates')

# Ruta del perfil de usuario
@perfil_usuario_bp.route("/perfil_usuario")
def perfil_usuario():
    # Si no hay sesión activa, redirige al login
    if 'user' not in session:
        flash("Por favor inicia sesión primero.", "warning")
        return redirect(url_for('main.demo_login'))  # o la ruta de tu login real

    # Obtener los datos de la sesión
    user_data = session['user']

    # Buscar el usuario real en la base de datos (por ID)
    usuario_db = Usuario.query.filter_by(idUsuario=user_data['id']).first()

    if usuario_db:
        usuario = {
            'nombre': usuario_db.usuario,
            'correo': usuario_db.correo,
            'rol': getattr(usuario_db, 'rol', 'Usuario estándar')
        }
    else:
        # Si no lo encuentra, usa los datos de sesión
        usuario = {
            'nombre': user_data.get('nombre', ''),
            'correo': user_data.get('correo', ''),
            'rol': user_data.get('rol', 'Usuario estándar')
        }

    return render_template("usuario/perfil_usuario.html", usuario=usuario)
