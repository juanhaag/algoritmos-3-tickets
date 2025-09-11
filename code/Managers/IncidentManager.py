from Models.Incident import Incident


class IncidentManager:

    def __init__(self):
        self.Incidents = []

    def create(self, description_, incidentNumber_):
        descripcion_Indicente = description_
        numero_Incidente = incidentNumber_
        nuevo_Incidente = Incident(descripcion_Indicente, numero_Incidente)
        self.Incidents.append(nuevo_Incidente)

    def modify(self, incidentNumber_, newDescription):
        incidentToModify = self.search(incidentNumber_)

        if incidentToModify:
            incidentToModify.descripcionIncidente = newDescription
        else:
            print("Incidente no encontra2")

    def search(self, incidentNumber_):
        for Incident in self.Incidents:
            if incidentNumber_ == Incident.numeroIncidente:
                return Incident
        return None

    def list(self):
        for Incident in self.Incidents:
            print(Incident)

    def show(self, incidentNumber_):
        print(self.search(incidentNumber_))

    def delete(self, incidentNumber_):
        incident = self.search(incidentNumber_)
        if incident:
            self.Incidents.remove(incident)
        else:
            print("Incidente no encontrado")

    # Aca van las de controlador

    def index(self):

        return None

    def store(self):

        return None

    def update(self):

        return None

    def destroy(self):

        return None
