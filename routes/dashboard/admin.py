from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.baseDatos import db, nuevaHabitacion, Usuario, nuevoPlato, Pedido
from flask import session
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Configuración de carpeta para imágenes de platos
UPLOAD_FOLDER_PLATOS = 'static/img/platos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta para mostrar formulario de edición de habitación
@admin_bp.route("/hospedaje/editar/<int:habitacion_id>", methods=["GET"])
def hospedaje_editar(habitacion_id):
    habitacion = nuevaHabitacion.query.get_or_404(habitacion_id)
    return render_template("dashboard/editar_habitacion.html", habitacion=habitacion)

# Ruta para actualizar habitación en la base de datos
@admin_bp.route("/hospedaje/editar/<int:habitacion_id>", methods=["POST"])
def hospedaje_actualizar(habitacion_id):
    habitacion = nuevaHabitacion.query.get_or_404(habitacion_id)
    try:
        habitacion.nombre = request.form["nombre"]
        habitacion.precio = float(request.form["precio"])
        habitacion.cupo_personas = int(request.form.get("cupo_personas", 1))
        habitacion.estado = request.form.get("estado", "Disponible")
        imagen_file = request.files.get("imagen")
        if imagen_file and imagen_file.filename:
            import os
            from werkzeug.utils import secure_filename
            filename = secure_filename(imagen_file.filename)
            img_folder = os.path.join("Static", "img")
            os.makedirs(img_folder, exist_ok=True)
            save_path = os.path.join(img_folder, filename)
            imagen_file.save(save_path)
            habitacion.imagen = f"img/{filename}"
        db.session.commit()
    # flash("✅ Habitación actualizada correctamente", "success")
    except Exception as e:
        db.session.rollback()
    # flash(f"❌ Error al actualizar la habitación: {e}", "danger")
    return redirect(url_for("admin.hospedaje_index"))
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.baseDatos import db, nuevaHabitacion, Usuario
from flask import session

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ==========================
# 📌 SECCIÓN HOSPEDAJE
# ==========================
@admin_bp.route("/hospedaje")
def hospedaje_index():
    habitaciones = nuevaHabitacion.query.all()
    return render_template("dashboard/hospedaje_admin.html", habitaciones=habitaciones)

#añadir nueva habitacion ---------------------------------------------------------

@admin_bp.route("/hospedaje/nueva", methods=["POST"])
def hospedaje_nueva():
    try:
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        print(f"[DEBUG] Descripción recibida: {descripcion}")
        precio = float(request.form["precio"])
        cupo_personas = int(request.form.get("cupo_personas", 1))
        estado = request.form.get("estado", "Disponible")
        imagen_file = request.files.get("imagen")
        imagen_path = None
        if imagen_file and imagen_file.filename:
            import os
            from werkzeug.utils import secure_filename
            filename = secure_filename(imagen_file.filename)
            img_folder = os.path.join("Static", "img")
            os.makedirs(img_folder, exist_ok=True)
            save_path = os.path.join(img_folder, filename)
            imagen_file.save(save_path)
            imagen_path = f"img/{filename}"

        habitacion = nuevaHabitacion(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            estado=estado,
            cupo_personas=cupo_personas,
            imagen=imagen_path
        )
        db.session.add(habitacion)
        db.session.commit()

        flash("✅ Habitación creada correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"❌ Error al crear la habitación: {e}", "danger")

    return redirect(url_for("admin.hospedaje_index"))

#editar habitacion ----------------------------------------------------------

@admin_bp.route("/hospedaje/editar/<int:habitacion_id>", methods=["POST"])
def hospedaje_editar(habitacion_id):
    habitacion = nuevaHabitacion.query.get_or_404(habitacion_id)
    try:
        habitacion.nombre = request.form["nombre"]
        habitacion.descripcion = request.form["descripcion"]
        habitacion.precio = float(request.form["precio"])
        habitacion.estado = request.form["estado"]
        habitacion.cupo_personas = int(request.form["cupo_personas"])
        db.session.commit()
        flash("✅ Habitación actualizada correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"❌ Error al editar la habitación: {e}", "danger")
    return redirect(url_for("admin.hospedaje_index"))

#eliminar habitacion ----------------------------------------------------------

@admin_bp.route("/hospedaje/eliminar/<int:habitacion_id>", methods=["POST"])
def hospedaje_eliminar(habitacion_id):
    habitacion = nuevaHabitacion.query.get_or_404(habitacion_id)
    try:
        db.session.delete(nuevaHabitacion)
        db.session.commit()
        flash("🗑️ Habitación eliminada", "warning")
    except Exception as e:
        db.session.rollback()
        flash(f"❌ Error al eliminar: {e}", "danger")

    return redirect(url_for("admin.hospedaje_index"))

# ==========================
# 📌 SECCIÓN RESTAURANTE
# ==========================
_platos_demo = []

@admin_bp.route("/home_dashboard")
def home_dashboard():
    return render_template("dashboard/home_dashboard.html")

@admin_bp.route("/restaurante")
def admin_restaurante():
    platos = nuevoPlato.query.all()
    return render_template("dashboard/restaurante_admin.html", platos=platos)

#añadir nuevo plato ---------------------------------------------------------

@admin_bp.route("/restaurante/nuevo", methods=["POST"])
def admin_restaurante_nuevo():
    try:
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        precio = float(request.form.get("precio") or 0)
        
        # Manejar la imagen
        imagen_filename = None
        if 'imagen' in request.files:
            imagen = request.files['imagen']
            if imagen and imagen.filename and allowed_file(imagen.filename):
                import uuid
                filename = f"{uuid.uuid4().hex}_{secure_filename(imagen.filename)}"
                
                # Crear carpeta si no existe
                from flask import current_app
                upload_dir = os.path.join(current_app.root_path, UPLOAD_FOLDER_PLATOS)
                os.makedirs(upload_dir, exist_ok=True)
                
                # Guardar imagen
                imagen.save(os.path.join(upload_dir, filename))
                imagen_filename = filename
        
        # Crear nuevo plato
        nuevo_plato = nuevoPlato(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            imagen=imagen_filename
        )
        db.session.add(nuevo_plato)
        db.session.commit()
        
        flash('Plato agregado exitosamente!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al agregar el plato: {str(e)}', 'danger')
    
    return redirect(url_for("admin.admin_restaurante"))

#editar plato ----------------------------------------------------------

@admin_bp.route("/restaurante/editar/<int:plato_id>", methods=["GET", "POST"])
def admin_restaurante_editar(plato_id):
    plato = nuevoPlato.query.get_or_404(plato_id)
    
    if request.method == "POST":
        try:
            plato.nombre = request.form.get("nombre")
            plato.descripcion = request.form.get("descripcion")
            plato.precio = float(request.form.get("precio") or 0)
            
            # Manejar la imagen
            if 'imagen' in request.files:
                imagen = request.files['imagen']
                if imagen and imagen.filename and allowed_file(imagen.filename):
                    import uuid
                    filename = f"{uuid.uuid4().hex}_{secure_filename(imagen.filename)}"
                    
                    from flask import current_app
                    upload_dir = os.path.join(current_app.root_path, UPLOAD_FOLDER_PLATOS)
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    imagen.save(os.path.join(upload_dir, filename))
                    plato.imagen = filename
            
            db.session.commit()
            flash('Plato actualizado exitosamente!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el plato: {str(e)}', 'danger')
        
        return redirect(url_for("admin.admin_restaurante"))

    platos = nuevoPlato.query.all()
    return render_template("dashboard/restaurante_admin.html", platos=platos, plato=plato)

#eliminar plato ----------------------------------------------------------

@admin_bp.route("/restaurante/eliminar/<int:plato_id>", methods=["POST"])
def admin_restaurante_eliminar(plato_id):
    try:
        plato = nuevoPlato.query.get_or_404(plato_id)
        db.session.delete(plato)
        db.session.commit()
        flash('Plato eliminado exitosamente!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el plato: {str(e)}', 'danger')
    
    return redirect(url_for("admin.admin_restaurante"))


# 📌 SECCIÓN PEDIDOS
# ------------------------------

@admin_bp.route("/pedidos")
def admin_pedidos():
    """Lista todos los pedidos, con opción de filtrar por estado"""
    filtro_estado = request.args.get('estado', None)
    
    if filtro_estado:
        pedidos = Pedido.query.filter_by(estado=filtro_estado).order_by(Pedido.id.desc()).all()
    else:
        pedidos = Pedido.query.order_by(Pedido.id.desc()).all()
    
    return render_template("dashboard/pedidos_admin.html", pedidos=pedidos, filtro_estado=filtro_estado)


@admin_bp.route("/pedidos/cambiar-estado/<int:pedido_id>", methods=["POST"])
def admin_pedido_cambiar_estado(pedido_id):
    """Cambia el estado de un pedido"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        nuevo_estado = request.form.get('estado')
        
        if nuevo_estado in ['Pendiente', 'En Preparación', 'Listo', 'Entregado']:
            pedido.estado = nuevo_estado
            db.session.commit()
            flash(f'Estado del pedido #{pedido_id} actualizado a: {nuevo_estado}', 'success')
        else:
            flash('Estado inválido', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar el pedido: {str(e)}', 'danger')
    
    return redirect(url_for("admin.admin_pedidos"))


@admin_bp.route("/pedidos/eliminar/<int:pedido_id>", methods=["POST"])
def admin_pedido_eliminar(pedido_id):
    """Elimina un pedido"""
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        db.session.delete(pedido)
        db.session.commit()
        flash('Pedido eliminado exitosamente!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el pedido: {str(e)}', 'danger')
    
    return redirect(url_for("admin.admin_pedidos"))
