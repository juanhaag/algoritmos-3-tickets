from flask import Flask, render_template, request, redirect
from Managers.ClientManager import ClientManager

app = Flask(__name__)
client_manager = ClientManager()

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



if __name__ == "__main__":
    app.run(debug=True)
