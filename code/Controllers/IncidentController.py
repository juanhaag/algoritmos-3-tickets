from flask import Blueprint, request, jsonify
from Database.database import db
from Models.Ticket import Ticket
from Models.Incident import Incident

incidents_bp = Blueprint('incidents', __name__)

@incidents_bp.route('/incidents', methods=['GET'])
def list_incidents():
    """
    @brief Obtiene una lista de todos los incidentes.
    
    @details Puede ser filtrada por el ID de un ticket si se proporciona
             el parámetro 'ticket_id' en la query string.
    
    @return Una respuesta JSON con la lista de incidentes.
    ---
    tags:
      - Incidents
    parameters:
      - in: query
        name: ticket_id
        type: integer
        description: Filtrar incidentes por ticket_id
    responses:
      200:
        description: Lista de incidentes
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              description:
                type: string
              priority:
                type: string
              status:
                type: string
              ticket_id:
                type: integer
              created_at:
                type: string
              updated_at:
                type: string
    """
    ticket_id = request.args.get('ticket_id', type=int)
    
    if ticket_id:
        incidents = Incident.query.filter_by(ticket_id=ticket_id).all()
    else:
        incidents = Incident.query.all()
    
    return jsonify([incident.to_dict() for incident in incidents])

@incidents_bp.route('/incidents', methods=['POST'])
def create_incident():
    """
    @brief Crea un nuevo incidente.
    
    @details Recibe los datos del incidente en formato JSON. Valida que los
             datos requeridos estén presentes y que el ticket asociado exista.
    
    @return Una respuesta JSON con el incidente creado y un código de estado 201.
    ---
    parameters:
      - in: body
        name: incident
        required: true
        schema:
          type: object
          required:
            - description
            - ticket_id
          properties:
            description:
              type: string
              description: Descripción del incidente
            priority:
              type: string
              description: Prioridad del incidente
              enum: [low, medium, high]
              default: medium
            status:
              type: string
              description: Estado del incidente
              enum: [open, in_progress, resolved, closed]
              default: open
            ticket_id:
              type: integer
              description: ID del ticket asociado
    responses:
      201:
        description: Incidente creado exitosamente
      400:
        description: Datos inválidos
      404:
        description: Ticket no encontrado
    """
    data = request.get_json()
    
    # --- Validación de datos de entrada ---
    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400
    if not data.get('description') or not str(data.get('description')).strip():
        return jsonify({'error': 'La descripción es requerida y no puede estar vacía'}), 400
    if not data.get('ticket_id') or not isinstance(data.get('ticket_id'), int):
        return jsonify({'error': 'Descripción y ticket_id son requeridos'}), 400
    
    allowed_priorities = {'low', 'medium', 'high'}
    allowed_statuses = {'open', 'in_progress', 'resolved', 'closed'}
    
    if 'priority' in data and data['priority'] not in allowed_priorities:
        return jsonify({'error': f"Prioridad inválida. Valores permitidos: {list(allowed_priorities)}"}), 400
    if 'status' in data and data['status'] not in allowed_statuses:
        return jsonify({'error': f"Estado inválido. Valores permitidos: {list(allowed_statuses)}"}), 400

    # Verificar que el ticket existe
    ticket = Ticket.query.get(data['ticket_id'])
    if not ticket:
        return jsonify({'error': 'Ticket no encontrado'}), 404
    
    incident = Incident(
        description=data['description'].strip(),
        priority=data.get('priority', 'medium'),
        status=data.get('status', 'open'),
        ticket_id=data['ticket_id']
    )
    
    db.session.add(incident)
    db.session.commit()
    
    return jsonify(incident.to_dict()), 201

@incidents_bp.route('/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    """
    @brief Obtiene un incidente específico por su ID.
    
    @param incident_id El ID del incidente a obtener.
    
    @return Una respuesta JSON con los datos del incidente o un 404 si no se encuentra.
    ---
    parameters:
      - in: path
        name: incident_id
        required: true
        type: integer
        description: ID del incidente
    responses:
      200:
        description: Incidente encontrado
      404:
        description: Incidente no encontrado
    """
    incident = Incident.query.get_or_404(incident_id)
    return jsonify(incident.to_dict())

@incidents_bp.route('/incidents/<int:incident_id>', methods=['PUT'])
def update_incident(incident_id):
    """
    @brief Actualiza un incidente existente.
    
    @details Recibe los campos a actualizar en formato JSON. Solo actualiza
             los campos permitidos y validados.
    
    @param incident_id El ID del incidente a actualizar.
    
    @return Una respuesta JSON con el incidente actualizado o un 404 si no se encuentra.
    ---
    parameters:
      - in: path
        name: incident_id
        required: true
        type: integer
        description: ID del incidente
      - in: body
        name: incident
        required: true
        schema:
          type: object
          properties:
            description:
              type: string
            priority:
              type: string
              enum: [low, medium, high]
            status:
              type: string
              enum: [open, in_progress, resolved, closed]
    responses:
      200:
        description: Incidente actualizado exitosamente
      404:
        description: Incidente no encontrado
    """
    incident = Incident.query.get_or_404(incident_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400
    
    # --- Lógica de actualización segura y validada ---
    allowed_updates = {
        'description': lambda v: isinstance(v, str) and v.strip(),
        'priority': lambda v: v in {'low', 'medium', 'high'},
        'status': lambda v: v in {'open', 'in_progress', 'resolved', 'closed'}
    }
    
    for key, value in data.items():
        if key in allowed_updates:
            if allowed_updates[key](value):
                setattr(incident, key, value.strip() if isinstance(value, str) else value)
            else:
                return jsonify({'error': f"Valor inválido para el campo '{key}'"}), 400

    db.session.commit()
    return jsonify(incident.to_dict())

@incidents_bp.route('/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    """
    @brief Elimina un incidente específico.
    
    @param incident_id El ID del incidente a eliminar.
    
    @return Una respuesta JSON confirmando la eliminación o un 404 si no se encuentra.
    ---
    parameters:
      - in: path
        name: incident_id
        required: true
        type: integer
        description: ID del incidente
    responses:
      200:
        description: Incidente eliminado exitosamente
      404:
        description: Incidente no encontrado
    """
    incident = Incident.query.get_or_404(incident_id)
    db.session.delete(incident)
    db.session.commit()
    return jsonify({'message': 'Incidente eliminado exitosamente'})
