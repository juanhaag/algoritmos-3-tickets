from Models.Incident import Incident


class IncidentManager:

    def __init__(self):
        self.Incidents = []

    def create(self, description_, incidentNumber_):
        nuevo_Incidente = Incident(description_, incidentNumber_)
        self.Incidents.append(nuevo_Incidente)

    def modify(self, incidentNumber_, newDescription):
        incidentToModify = self.search(incidentNumber_)

        if incidentToModify:
            incidentToModify.DescripcionIncidente = newDescription
        else:
            print("Incidente no encontra2")

    def search(self, incidentNumber_):
        for Incident in self.Incidents:
            if incidentNumber_ == Incident.NumeroIncidente:
                return Incident
        return None

    def list(self):
        return self.Incidents

    def show(self, incidentNumber_):
        print(self.search(incidentNumber_))

    def delete(self, incidentNumber_):
        incident = self.search(incidentNumber_)
        if incident:
            self.Incidents.remove(incident)
        else:
            print("Incidente no encontrado")

