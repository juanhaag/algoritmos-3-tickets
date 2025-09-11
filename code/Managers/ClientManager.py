from Models.Client import Client


class ClientManager:

    def __init__(self):
        self.Clients = []

    def create(self):
        nombreCliente = "placeholder"
        idCliente = 1
        nuevo_cliente = Client(nombreCliente, idCliente)
        self.Clients.append(nuevo_cliente)


    def modify(self, client_id, newName):
        client = self.search(client_id)
        if client:
            client.name_Cliente = newName
        else:
            print("Cliente no encontrado")

    def search(self, client_id):
        for client in self.Clients:
            if client.id_Cliente == client_id:
                return client
        return None

    def list(self):
        return self.Clients

    def delete(self, client_id):
        client = self.search(client_id)
        if client:
            self.Clients.remove(client)
            print(f"Cliente {client_id} eliminado")
        else:
            print("Cliente no encontrado")

 
    def index(self):
        return self.list()

    def store(self, nombre, client_id):
        # No tengo idea que se supone que hace store
        if self.search(client_id):
            print("Cliente ya existe")
            return None
        nuevo_cliente = Client(nombre, client_id)
        self.Clients.append(nuevo_cliente)
        return nuevo_cliente

    def show(self, client_id):
        client = self.search(client_id)
        if client:
            return client
        print("Cliente no encontrado")
        return None

    def update(self, client_id, newName):
        # No tengo idea que hace update xq ya existe modificar
        self.modify(client_id, newName)

    def destroy(self, client_id):
        # No tengo idea la diferencia entre eliminar y destruir
        self.delete(client_id)
