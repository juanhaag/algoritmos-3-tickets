from Models.Service import Service

class ServiceManager:
    def __init__(self):
            self.Services = []

    def create(self,description_, price_):
        ServiceDescription = description_
        ServicePrice = price_
        nuevo_Service = Service(ServiceDescription, ServicePrice)
        self.Services.append(nuevo_Service)


    def modify(self, Service_id, newName):
        Service = self.search(Service_id)
        if Service:
            Service.name_Service = newName
        else:
            print("Service no encontrado")

    def search(self, Service_id):
        for Service in self.Services:
            if Service.id_Service == Service_id:
                return Service
        return None

    def list(self):
        return self.Services

    def delete(self, Service_id):
        Service = self.search(Service_id)
        if Service:
            self.Services.remove(Service)
            print(f"Service {Service_id} eliminado")
        else:
            print("Service no encontrado")

