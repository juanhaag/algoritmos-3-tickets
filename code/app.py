from flask import Flask, render_template, request, redirect
from Managers.ClientManager import ClientManager
from Repositories.TicketRepository import TicketRepository

app = Flask(__name__)
client_manager = ClientManager()
ticket_repo = TicketRepository()

@app.route("/")
def home():
    return "Index page"


@app.route("/login")
def login():
    return "Login page"

#///////////PRUEBAS DE CLIENTE/////////////////////////////

@app.route("/prueba-cliente")
def prueba_cliente():
    return render_template("prueba_cliente.html", clients=client_manager.list())



@app.route("/prueba-cliente/create", methods=["POST"])
def create_client():
    client_manager.create()
    return redirect("/prueba-cliente")


@app.route("/prueba-cliente/modify", methods=["POST"])
def modify_client():
    client_id = int(request.form.get("id"))
    new_name = request.form.get("newName")
    client_manager.modify(client_id, new_name)
    return redirect("/prueba-cliente")


@app.route("/prueba-cliente/delete", methods=["POST"])
def delete_client():
    client_id = int(request.form.get("id"))
    client_manager.delete(client_id)
    return redirect("/prueba-cliente")


#///////////PRUEBAS DE INCIDENTE/////////////////////////////

@app.route("/prueba-incidente")
def prueba_incidente():
    return render_template("prueba_incidente.html")


@app.route('/tickets', methods=['GET'])
def list_tickets():
    return ticket_repo.get_all()


@app.route('/tickets', methods=['POST'])
def create_ticket():
    payload = request.get_json() or {}
    client = payload.get('client')
    incident = payload.get('incident')
    message = payload.get('message', '')
    ticket_id = ticket_repo.create(client=client, incident=incident, message=message)
    return { 'id': ticket_id }, 201


@app.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    t = ticket_repo.get_by_id(ticket_id)
    if not t:
        return { 'error': 'Not found' }, 404
    return t


@app.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    payload = request.get_json() or {}
    updated = ticket_repo.update(ticket_id, **payload)
    if not updated:
        return { 'error': 'Not found or no valid fields provided' }, 400
    return { 'updated': True }


@app.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    deleted = ticket_repo.delete(ticket_id)
    if not deleted:
        return { 'error': 'Not found' }, 404
    return { 'deleted': True }


if __name__ == "__main__":
    app.run(debug=True)
