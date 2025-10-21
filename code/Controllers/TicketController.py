from flask import Blueprint, request, jsonify
from Database.database import db
from Models.Ticket import Ticket
from Models.Incident import Incident

tickets_bp = Blueprint("tickets", __name__)


@tickets_bp.route("/tickets", methods=["GET"])
def list_tickets():
    """
    @brief Obtiene una lista de todos los tickets.

    @details Cada ticket en la lista incluye sus incidentes asociados.

    @return Una respuesta JSON con la lista de tickets.
    ---
    tags:
      - Tickets
    responses:
      200:
        description: Lista de todos los tickets con sus incidentes
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              description:
                type: string
              client_name:
                type: string
              state:
                type: string
              created_at:
                type: string
              updated_at:
                type: string
              incidents:
                type: array
                items:
                  type: object
    """
    tickets = Ticket.query.all()
    return jsonify([ticket.to_dict() for ticket in tickets])


@tickets_bp.route("/tickets", methods=["POST"])
def create_ticket():
    """
    @brief Crea un nuevo ticket.

    @details Recibe los datos del ticket en formato JSON. Valida que los
             campos requeridos (título y nombre del cliente) estén presentes.

    @return Una respuesta JSON con el ticket creado y un código de estado 201.
    ---
    tags:
      - Tickets
    parameters:
      - in: body
        name: ticket
        required: true
        schema:
          type: object
          required:
            - title
            - client_name
          properties:
            title:
              type: string
              description: Título del ticket
            description:
              type: string
              description: Descripción del ticket
            client_name:
              type: string
              description: Nombre del cliente (hardcodeado)
            telephone_operator_name:
              type: string
              description: Nombre del operador telefónico (hardcodeado)
              default: Operador Hardcodeado
            technician_name:
              type: string
              description: Nombre del técnico (hardcodeado)
              default: Técnico Hardcodeado
            unit_equipment_name:
              type: string
              description: Nombre del equipo (hardcodeado)
              default: Equipo Hardcodeado
            state:
              type: string
              description: Estado del ticket (hardcodeado)
              default: open
            service_record_description:
              type: string
              description: Descripción del registro de servicio (hardcodeado)
              default: Registro de servicio hardcodeado
            message_content:
              type: string
              description: Contenido del mensaje (hardcodeado)
              default: Mensaje hardcodeado
    responses:
      201:
        description: Ticket creado exitosamente
      400:
        description: Datos inválidos
    """
    data = request.get_json()

    # --- Validación de datos de entrada ---
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    if not data.get("title") or not str(data.get("title")).strip():
        return jsonify({"error": "El título es requerido y no puede estar vacío"}), 400
    if not data.get("client_name") or not str(data.get("client_name")).strip():
        return jsonify({"error": "Título y nombre del cliente son requeridos"}), 400

    # --- Creación del objeto Ticket con todos los datos ---
    ticket = Ticket(
        title=data["title"],
        client_name=data["client_name"],
        description=data.get("description", ""),
        telephone_operator_name=data.get(
            "telephone_operator_name", "Operador Hardcodeado"
        ),
        technician_name=data.get("technician_name", "Técnico Hardcodeado"),
        unit_equipment_name=data.get("unit_equipment_name", "Equipo Hardcodeado"),
        state=data.get("state", "open"),
        service_record_description=data.get(
            "service_record_description", "Registro de servicio hardcodeado"
        ),
        message_content=data.get("message_content", "Mensaje hardcodeado"),
    )

    db.session.add(ticket)
    db.session.commit()

    return jsonify(ticket.to_dict()), 201


@tickets_bp.route("/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    """
    @brief Obtiene un ticket específico por su ID.

    @param ticket_id El ID del ticket a obtener.

    @return Una respuesta JSON con los datos del ticket o un 404 si no se encuentra.
    ---
    tags:
      - Tickets
    parameters:
      - in: path
        name: ticket_id
        required: true
        type: integer
        description: ID del ticket
    responses:
      200:
        description: Ticket encontrado
      404:
        description: Ticket no encontrado
    """
    ticket = Ticket.query.get_or_404(ticket_id)
    return jsonify(ticket.to_dict())


@tickets_bp.route("/tickets/<int:ticket_id>", methods=["PUT"])
def update_ticket(ticket_id):
    """
    @brief Actualiza un ticket existente.

    @details Recibe los campos a actualizar en formato JSON. Solo actualiza
             los campos permitidos y validados.

    @param ticket_id El ID del ticket a actualizar.

    @return Una respuesta JSON con el ticket actualizado o un 404 si no se encuentra.
    ---
    tags:
      - Tickets
    parameters:
      - in: path
        name: ticket_id
        required: true
        type: integer
        description: ID del ticket
      - in: body
        name: ticket
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            client_name:
              type: string
            telephone_operator_name:
              type: string
            technician_name:
              type: string
            unit_equipment_name:
              type: string
            state:
              type: string
            service_record_description:
              type: string
            message_content:
              type: string
    responses:
      200:
        description: Ticket actualizado exitosamente
      404:
        description: Ticket no encontrado
    """
    ticket = Ticket.query.get_or_404(ticket_id)
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    # --- Lógica de actualización segura y validada ---
    allowed_updates = {
        "title": lambda v: isinstance(v, str) and v.strip(),
        "description": lambda v: isinstance(v, str),
        "client_name": lambda v: isinstance(v, str) and v.strip(),
        "telephone_operator_name": lambda v: isinstance(v, str),
        "technician_name": lambda v: isinstance(v, str),
        "unit_equipment_name": lambda v: isinstance(v, str),
        "state": lambda v: v in {"open", "in_progress", "resolved", "closed"},
        "service_record_description": lambda v: isinstance(v, str),
        "message_content": lambda v: isinstance(v, str),
    }

    for key, value in data.items():
        if key in allowed_updates:
            if allowed_updates[key](value):
                setattr(ticket, key, value.strip() if isinstance(value, str) else value)
            else:
                return jsonify({"error": f"Valor inválido para el campo '{key}'"}), 400

    db.session.commit()
    return jsonify(ticket.to_dict())


@tickets_bp.route("/tickets/<int:ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):
    """
    @brief Elimina un ticket y sus incidentes asociados.

    @details Gracias a la configuración 'cascade' en el modelo, al eliminar
             un ticket, SQLAlchemy también elimina todos sus incidentes.

    @param ticket_id El ID del ticket a eliminar.

    @return Una respuesta JSON confirmando la eliminación o un 404 si no se encuentra.
    ---
    tags:
      - Tickets
    parameters:
      - in: path
        name: ticket_id
        required: true
        type: integer
        description: ID del ticket
    responses:
      200:
        description: Ticket eliminado exitosamente
      404:
        description: Ticket no encontrado
    """
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": "Ticket eliminado exitosamente"})
