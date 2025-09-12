from Models.Service import Service

class ServiceManager:
    def __init__(self, category_, categoryId_):
            self.Services = []
            self.Category = category_
            self.CategoryId = categoryId_

    def create(self,Description_, Price_, ServiceId_, ServiceName_):
        nuevo_Service = Service(Description_, Price_, ServiceId_, ServiceName_)
        self.Services.append(nuevo_Service)


    def modify(self, Service_id, newName_, newDescription_, newPrice_):
        Service = self.search(Service_id)
        if Service:
            Service.Name = newName_
            Service.Description = newDescription_
            Service.Price = newPrice_
        else:
            print("Service no encontrado")

    def search(self, Service_id):
        for Service in self.Services:
            if Service.Id == Service_id:
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

