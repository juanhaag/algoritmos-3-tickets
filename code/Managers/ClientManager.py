from Models.Client import Client


class ClientManager:

    def __init__(self):
        self.Clients = []

    def create(self, Name_, Id_):
        nuevoCliente = Client(Name_, Id_)
        self.Clients.append(nuevoCliente)


    def modify(self, clientId, newName):
        client = self.search(clientId)
        if client:
            client.Name = newName
        else:
            print("Cliente no encontrado")

    def search(self, clientId_):
        for client in self.Clients:
            if client.ClientId == clientId_:
                return client
        return None

    def list(self):
        return self.Clients

    def delete(self, clientId):
        client = self.search(clientId)
        if client:
            self.Clients.remove(client)
            print(f"Cliente {clientId} eliminado")
        else:
            print("Cliente no encontrado")

