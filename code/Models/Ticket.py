from Database.database import db
from datetime import datetime
from typing import List, TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .Incident import Incident

class Ticket(db.Model):
    """
    @brief Modelo de datos para un Ticket.
    
    @details Representa un ticket de soporte que agrupa uno o más incidentes.
             Para fines educativos, muchos de sus campos son hardcodeados.
    """
    __tablename__ = 'tickets'
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(db.Text, nullable=True)
    
    # Campos hardcodeados según el diagrama UML
    client_name: Mapped[str] = mapped_column(db.String(100), nullable=False)  # Cliente hardcodeado
    telephone_operator_name: Mapped[Optional[str]] = mapped_column(db.String(100), default='Operador Hardcodeado')  # TelephoneOperator hardcodeado
    technician_name: Mapped[Optional[str]] = mapped_column(db.String(100), default='Técnico Hardcodeado')  # Technician hardcodeado
    unit_equipment_name: Mapped[Optional[str]] = mapped_column(db.String(100), default='Equipo Hardcodeado')  # UnitEquipment hardcodeado
    state: Mapped[Optional[str]] = mapped_column(db.String(50), default='open')  # State hardcodeado
    service_record_description: Mapped[Optional[str]] = mapped_column(db.Text, default='Registro de servicio hardcodeado', nullable=True)  # ServiceRecord hardcodeado
    message_content: Mapped[Optional[str]] = mapped_column(db.Text, default='Mensaje hardcodeado', nullable=True)  # Message hardcodeado
    
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación 1:N con Incident
    incidents: Mapped[List["Incident"]] = relationship(backref='ticket', lazy=True, cascade='all, delete-orphan')

    def __init__(self, title, client_name, description=None, 
                 telephone_operator_name=None, technician_name=None, 
                 unit_equipment_name=None, state=None, 
                 service_record_description=None, message_content=None):
        """
        @brief Constructor explícito para la clase Ticket.
        
        @details Este constructor se define para compatibilidad con herramientas de
                 análisis estático como Pylance, que no detectan el __init__
                 automático de SQLAlchemy.
        """
        self.title = title
        self.client_name = client_name
        self.description = description
        self.telephone_operator_name = telephone_operator_name
        self.technician_name = technician_name
        self.unit_equipment_name = unit_equipment_name
        self.state = state
        self.service_record_description = service_record_description
        self.message_content = message_content

    def to_dict(self):
        """
        @brief Convierte el objeto Ticket a un diccionario.
        
        @details Serializa el ticket y su lista de incidentes asociados,
                 lo que es ideal para las respuestas de la API.
        
        @return Un diccionario que representa el ticket y sus incidentes.
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'client_name': self.client_name,
            'telephone_operator_name': self.telephone_operator_name,
            'technician_name': self.technician_name,
            'unit_equipment_name': self.unit_equipment_name,
            'state': self.state,
            'service_record_description': self.service_record_description,
            'message_content': self.message_content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'incidents': [incident.to_dict() for incident in self.incidents]
        }
    
    def __repr__(self):
        return f'<Ticket {self.id}: {self.title}>'