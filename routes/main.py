from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from datetime import datetime
from models.baseDatos import db,nuevaHabitacion
import os
from werkzeug.utils import secure_filename
from flask import current_app



main_bp = Blueprint('main', __name__)

#Rutas Home ---------------------------------------------------------
 
@main_bp.route('/')
def home():
    return render_template('home/Home.html')

@main_bp.route('/hospedaje')
def hospedaje():
    habitaciones = nuevaHabitacion.query.all()
    return render_template('home/Hospedaje.html', habitaciones=habitaciones)



@main_bp.route('/restaurante')
def restaurantes():
    return render_template('home/Restaurante.html')

@main_bp.route('/nosotros')
def nosotros():
    return render_template('home/Nosotros.html')

@main_bp.route('/Experiencias', methods=['GET', 'POST'])
def experiencias():
    comentarios = []
    if request.method == 'POST':
        contenido = request.form.get('contenido')
        rating = request.form.get('rating', 0)
        # Import current_user lazily to avoid hard dependency on flask_login at import time
        try:
            from flask_login import current_user
        except Exception:
            current_user = None

        if current_user and getattr(current_user, 'is_authenticated', False):
            username = getattr(current_user, 'usuario', None) or getattr(current_user, 'username', None) or session.get('user', {}).get('nombre')
            nuevo = {
                'user': {'username': username or 'Anónimo', 'avatar': None},
                'contenido': contenido,
                'rating': int(rating) if rating else 0,
                'created_at': datetime.now()
            }
            comentarios.append(nuevo)
    return render_template('home/Experiencias.html', comentarios=comentarios)

#Rutas Usuario -----------------------------------------------------------

@main_bp.route('/home_usuario')
def home_usuario():
    return render_template('usuario/home_usuario.html')

@main_bp.route('/hospedaje_usuario')
def hospedaje_usuario():
    habitaciones = nuevaHabitacion.query.all()
    return render_template('usuario/hospedaje_usuario.html', habitaciones=habitaciones)


@main_bp.route('/restaurante_usuario')
def restaurante_usuario():
    return render_template('usuario/restaurante_usuario.html')

@main_bp.route('/experiencias_usuario')
def experiencias_usuario():
    return render_template('usuario/experiencias_usuario.html')

@main_bp.route('/nosotros_usuario')
def nosotros_usuario():
    return render_template('usuario/nosotros_usuario.html')
# ...existing code...

#@main_bp.route('/perfil_usuario')
#def perfil_usuario():
    #return render_template('usuario/perfil_usuario.html')


#Rutas Admin ------------------------------------------------------------

@main_bp.route('/home_admin')
def home_admin():
    return render_template('dashboard/home_admin.html')

@main_bp.route('/hospedaje_admin')
def hospedaje_admin():
    habitaciones = nuevaHabitacion.query.all()
    return render_template('dashboard/hospedaje_admin.html', habitaciones=habitaciones)

@main_bp.route('/restaurante_admin')
def restaurante_admin():
    return render_template('dashboard/restaurante_admin.html')

@main_bp.route('/experiencias_admin')
def experiencias_admin():
    return render_template('dashboard/experiencias_admin.html')

@main_bp.route('/nosotros_admin')
def nosotros_admin():
    return render_template('dashboard/nosotros_admin.html')

@main_bp.route('/hospedaje_admin/eliminar/<int:habitacion_id>', methods=['POST'])
def eliminar_habitacion_admin(habitacion_id):
    habitacion = nuevaHabitacion.query.get_or_404(habitacion_id)
    # Elimina la habitación de la base de datos
    from models.baseDatos import db  # importa tu objeto db si no está importado
    db.session.delete(habitacion)
    db.session.commit()
    return redirect(url_for('main.hospedaje_admin'))

@main_bp.route('/hospedaje_admin/editar/<int:habitacion_id>', methods=['GET', 'POST'])
def editar_habitacion_admin(habitacion_id):
    habitacion = nuevaHabitacion.query.get_or_404(habitacion_id)

    if request.method == 'POST':
        # Actualiza los campos de la habitación
        habitacion.nombre = request.form.get('nombre', habitacion.nombre)
        habitacion.precio = request.form.get('precio', habitacion.precio)
        habitacion.cupo_personas = request.form.get('cupo_personas', habitacion.cupo_personas)
        habitacion.estado = request.form.get('estado', habitacion.estado)
        habitacion.descripcion = request.form.get('descripcion', habitacion.descripcion)

        # Manejo de imagen (si se sube una nueva)
        imagen = request.files.get('imagen')
        if imagen and imagen.filename:
            filename = secure_filename(imagen.filename)
            upload_dir = os.path.join(current_app.root_path, 'static', 'img')
            os.makedirs(upload_dir, exist_ok=True)
            save_path = os.path.join(upload_dir, filename)
            imagen.save(save_path)

            # Borrar imagen vieja si existe y no es el placeholder/default
            try:
                old = habitacion.imagen  # p.ej. "img/old.jpg" o None
                if old:
                    old_path = os.path.join(current_app.root_path, 'static', old)
                    if os.path.exists(old_path) and os.path.isfile(old_path):
                        # evita borrar un default si tu placeholder contiene "default" en el nombre
                        if 'default' not in os.path.basename(old_path).lower():
                            os.remove(old_path)
            except Exception as e:
                current_app.logger.warning(f"Error al eliminar imagen anterior: {e}")

            # Guarda la ruta relativa a static/ en la BD (consistente con tu uso actual)
            habitacion.imagen = f"img/{filename}"

        # Guardar cambios en BD
        try:
            db.session.commit()
            flash('Habitación actualizada correctamente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la habitación: {e}', 'danger')

        return redirect(url_for('main.hospedaje_admin'))

    # GET -> renderizar formulario con datos actuales
    return render_template('dashboard/editar_habitacion.html', habitacion=habitacion)

@main_bp.route('/hospedaje/actualizar/<int:habitacion_id>', methods=['POST'])
def hospedaje_actualizar(habitacion_id):
    habitacion = nuevaHabitacion.query.get(habitacion_id)
    if habitacion:
        habitacion.nombre = request.form['nombre']
        habitacion.precio = request.form['precio']
        # ... actualizas lo demás
        db.session.commit()
    return redirect(url_for('main.hospedaje_admin'))


# Ruta de login demo para pruebas rápidas ---------------------------------

@main_bp.route('/demo-login', methods=['GET', 'POST'])
def demo_login():
    # Demo login kept for quick testing under /demo-login
    if request.method == 'POST':
        username = request.form.get('usuario')
        password = request.form.get('password')

        if username == "admin" and password == "1234":
            session['rol'] = 'admin'
            return redirect(url_for('main.home_admin'))
        else:
            session['rol'] = 'usuario'
            return redirect(url_for('main.home_usuario'))

    return render_template('home/Login.html')