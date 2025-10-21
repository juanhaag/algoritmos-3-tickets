from .Technician import Technician
from .Service import Service
from datetime import datetime

class ServiceRecord:
    """Represents a work log entry tying a `Technician` to a `Service`.
    """
    def __init__(self, technician: Technician, service: Service, notes: str = ""):
        self.technician = technician
        self.service = service
        self.notes = notes
        self.performed_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "technician": self.technician.to_dict() if hasattr(self.technician, 'to_dict') else None,
            "service": self.service.to_dict() if hasattr(self.service, 'to_dict') else None,
            "notes": self.notes,
            "performed_at": self.performed_at,
        }
