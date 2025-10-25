from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utils.extensions import db

# ------------------------------
# Tabla de Usuario
# ------------------------------
class Usuario(db.Model):
    __tablename__ = 'usuario'
    idUsuario = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(255), nullable=False)
    correo = db.Column(db.String(255), nullable=True, unique=True)
    contrasena = db.Column(db.String(255), nullable=False)  
    direccion = db.Column(db.String(255), nullable=True)
    fechaNacimiento = db.Column(db.Date, nullable=True)
    rol = db.Column(db.String(20), nullable=True, default='usuario')
    imagen = db.Column(db.String(200), nullable=True)


    def __repr__(self):
        return f"<Usuario {self.usuario}>"


# ------------------------------
# Tabla de nuevaHabitaciones
# ------------------------------
class nuevaHabitacion(db.Model):
    __tablename__ = "nuevaHabitacion"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default="Disponible")
    cupo_personas = db.Column(db.Integer, nullable=False, default=1)
    imagen = db.Column(db.String(255), nullable=True)  # ✅ AGREGA ESTA LÍNEA
    
    def __repr__(self):
        return f"<nuevaHabitacion {self.nombre} - {self.estado}>"
    
    

# ------------------------------
# Tabla de habitacioneHuesped
# ------------------------------

class habitacionHuesped(db.Model):
    __tablename__ = "habitacionHuesped"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    cantidad_personas = db.Column(db.Integer, nullable=False, default=1)
    check_in = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    check_out = db.Column(db.Date, nullable=True)
    

    def __repr__(self):
        return f"<HabitacionHuesped {self.nombre} - {self.check_in} to {self.check_out}>"
    
    
    
# ------------------------------
# Tabla de Huéspedes
# ------------------------------
class Huesped(db.Model):
    __tablename__ = "huesped"

    idHuesped = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipoDocumento = db.Column(db.String(50), nullable=False)
    numeroDocumento = db.Column(db.Integer, nullable=False, unique=True)
    telefono = db.Column(db.String(20), nullable=True)
    correo = db.Column(db.String(255), nullable=True)
    procedencia = db.Column(db.String(100), nullable=True)
    nuevaHabitacion_id = db.Column(db.Integer, db.ForeignKey("nuevaHabitacion.id"), nullable=False)
    
    # Relación con nuevaHabitacion
    habitacion = db.relationship('nuevaHabitacion', backref='huespedes', lazy=True)

    def __repr__(self):
        return f"<Huesped {self.nombre} en habitacion {self.nuevaHabitacion_id}>"
    


"""# ------------------------------
# Tabla de Restaurantes
# ------------------------------
class Restaurante(db.Model):
    __tablename__ = "restaurantes"

    idRestaurante = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo_comida = db.Column(db.String(100), nullable=False)
    horario = db.Column(db.String(50), nullable=True)

    def __repr__(self):
    return f"<Restaurante {self.nombre}>"
    """

# ------------------------------
# Tabla de Estadísticas
# ------------------------------
class Estadistica(db.Model):
    __tablename__ = "estadistica"

    idEstadistica = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    total_habitaciones = db.Column(db.Integer, nullable=False, default=0)
    habitaciones_ocupadas = db.Column(db.Integer, nullable=False, default=0)
    habitaciones_disponibles = db.Column(db.Integer, nullable=False, default=0)
    total_huespedes = db.Column(db.Integer, nullable=False, default=0)
    ingresos_totales = db.Column(db.Float, nullable=False, default=0.0)
    ocupacion_porcentaje = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return f"<Estadistica {self.fecha} - Ocupación: {self.ocupacion_porcentaje}%>"

# ------------------------------
# Tabla de Platos
# ------------------------------
class nuevoPlato(db.Model):
    __tablename__ = "nuevoplato"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Float, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<nuevoPlato {self.nombre} - ${self.precio}>"


# Tabla de Pedidos
# ------------------------------
class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nuevoPlato_id = db.Column(db.Integer, db.ForeignKey('nuevoplato.id'), nullable=False)
    nombreCliente = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    checkin = db.Column(db.Date, nullable=False)
    checkout = db.Column(db.Date, nullable=False)
    # Hora elegida por el usuario (zona local de Colombia)
    hora_reserva = db.Column(db.Time, nullable=True)
    instrucciones = db.Column(db.Text, nullable=True)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='Pendiente')  # Pendiente, En Preparación, Listo, Entregado

    # Relación con plato
    plato = db.relationship('nuevoPlato', backref='pedidos', lazy=True)

    def __repr__(self):
        return f"<Pedido {self.id} - {self.nombreCliente} - {self.estado}>"