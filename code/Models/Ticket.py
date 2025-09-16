from TelephoneOperator import TelephoneOperator
from ServiceRecord import ServiceRecord
from Incident import Incident
from Message import Message
from State import State
from Client import Client
from UnitEquipment import UnitEquipment
from Managers.TicketManager import TicketManager
from datetime import datetime

class Ticket:
    def __init__(self, id:int, client:Client, incident: Incident):
        self.id = id
        self.client = client
        self.incident = incident
        self.telephone_operator = None
        self.service_record = None
        self.message = ""
        self.state = "open"
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.noew().isoformat()

#Convertir la instancia  en un diccionario para convertilo a Json
    def to_dict(self):
        return{
            "id": self.id,
            "client": self.client.todict() if self.client else None,
            "incident": self.incident.todict() if self.incident else None,
            "telephone_operator": self.telephone_operator,
            "service_record": self.service_record,
            "message": self.message,
            "state": self.state,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

