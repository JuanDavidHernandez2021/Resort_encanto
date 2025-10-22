from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.baseDatos import db, nuevaHabitacion, Huesped
from datetime import datetime

hospedaje_usuario_bp = Blueprint('hospedaje_usuario', __name__)

@hospedaje_usuario_bp.route('/hospedaje_usuario')
def hospedaje_usuario():
    habitaciones = nuevaHabitacion.query.all()
    return render_template('usuario/hospedaje_usuario.html', habitaciones=habitaciones)


@hospedaje_usuario_bp.route('/reservar/<int:habitacion_id>', methods=['POST'])
def reservar_habitacion(habitacion_id):
    habitacion = nuevaHabitacion.query.get_or_404(habitacion_id)
    
    # Verificar si la habitación ya está ocupada
    if habitacion.estado == "Ocupada":
        flash('Lo sentimos, esta habitación ya está reservada. Por favor elige otra.', 'warning')
        return redirect(url_for('hospedaje_usuario.hospedaje_usuario'))
    
    # Obtener datos del formulario
    numero_documento = request.form['numeroDocumento']
    
    # Verificar si el huésped ya existe
    huesped_existente = Huesped.query.filter_by(numeroDocumento=numero_documento).first()
    
    if huesped_existente:
        # Actualizar la habitación del huésped existente
        huesped_existente.nuevaHabitacion_id = habitacion.id
        huesped_existente.nombre = request.form['nombre']
        huesped_existente.tipoDocumento = request.form['tipoDocumento']
        huesped_existente.telefono = request.form.get('telefono')
        huesped_existente.correo = request.form.get('correo')
        huesped_existente.procedencia = request.form.get('procedencia')
    else:
        # Crear nuevo huésped
        huesped = Huesped(
            nombre=request.form['nombre'],
            tipoDocumento=request.form['tipoDocumento'],
            numeroDocumento=numero_documento,
            telefono=request.form.get('telefono'),
            correo=request.form.get('correo'),
            procedencia=request.form.get('procedencia'),
            nuevaHabitacion_id=habitacion.id
        )
        db.session.add(huesped)
    
    # Cambiar el estado de la habitación a "Ocupada"
    habitacion.estado = "Ocupada"
    db.session.commit()
    
    flash('¡Reservación exitosa! Tu reserva ha sido confirmada.', 'success')
    return redirect(url_for('hospedaje_usuario.hospedaje_usuario'))
