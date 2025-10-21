from Database.database import db
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

class Incident(db.Model):
    """
    @brief Modelo de datos para un Incidente.
    
    @details Representa un incidente específico que está asociado a un Ticket.
             Contiene detalles como descripción, prioridad y estado.
    """
    __tablename__ = 'incidents'
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    description: Mapped[str] = mapped_column(db.Text, nullable=False)
    priority: Mapped[str] = mapped_column(db.String(20), default='medium')  # low, medium, high
    status: Mapped[str] = mapped_column(db.String(20), default='open')  # open, in_progress, resolved, closed
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Clave foránea hacia Ticket (relación N:1)
    ticket_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    
    def __init__(self, description, ticket_id, priority='medium', status='open'):
        """
        @brief Constructor para la clase Incident.
        
        @param description Descripción detallada del incidente.
        @param ticket_id ID del Ticket al que está asociado este incidente.
        @param priority Prioridad del incidente (low, medium, high).
        @param status Estado actual del incidente (open, in_progress, resolved, closed).
        """
        self.description = description
        self.ticket_id = ticket_id
        self.priority = priority
        self.status = status

    def to_dict(self):
        """
        @brief Convierte el objeto Incident a un diccionario.
        
        @details Útil para la serialización a formato JSON en las respuestas de la API.
        
        @return Un diccionario que representa el incidente.
        """
        return {
            'id': self.id,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'ticket_id': self.ticket_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Incident {self.id}: {self.description[:50]}...>'