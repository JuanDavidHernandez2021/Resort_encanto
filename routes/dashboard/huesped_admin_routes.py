from flask import Blueprint, render_template
from models.baseDatos import db, Huesped

huesped_admin_bp = Blueprint('huesped_admin', __name__)

@huesped_admin_bp.route('/huesped')
def mostrar_huespedes():
    huespedes = Huesped.query.all()
    return render_template('dashboard/huesped_admin.html', huespedes=huespedes)
