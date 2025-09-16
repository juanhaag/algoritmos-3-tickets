from Models.Technician import Technician

class TechnicianManager:
    """Class TechnicianManager
    """

    def __init__(self):
        self.technicians = []

    def create(self, id: str, name: str, surname: str, phone: str):

        newTechnician = Technician(id, name, surname, phone)
        self.technicians.append(newTechnician)

    
    def modify(self, id: str, name: str, surname: str, phone: str):
        technician = self.search(id)
        if technician:
            technician.name = name
            technician.surname = surname
            technician.phone = phone
        # else:
            # print("Technician no encontrado")
    
    def search(self, id: str):
        for technician in self.technicians:
            if technician.id == id:
                return technician
            # else:
                # print("Technician no encontrado")

    
    def list(self):
        return self.technicians
    
    def delete(self):
        technician = self.search(id)
        if technician:
            self.technicians.remove(technician)
        # else:
            # print("Technician no encontrado")    