from flask import Blueprint, request, jsonify
from Database.database import db
from Models.Ticket import Ticket
from Models.Incident import Incident

tickets_bp = Blueprint('tickets_bp', __name__)

@tickets_bp.route('/tickets', methods=['GET'])
def list_tickets():
    """
    @brief Obtiene una lista de todos los tickets.
    
    @details Cada ticket en la lista incluye sus incidentes asociados.
    
    @return Una respuesta JSON con la lista de tickets.
    ---
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

@tickets_bp.route('/tickets', methods=['POST'])
def create_ticket():
    """
    @brief Crea un nuevo ticket.
    
    @details Recibe los datos del ticket en formato JSON. Valida que los
             campos requeridos (título y nombre del cliente) estén presentes.
    
    @return Una respuesta JSON con el ticket creado y un código de estado 201.
    ---
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
        return jsonify({'error': 'No se proporcionaron datos'}), 400
    if not data.get('title') or not str(data.get('title')).strip():
        return jsonify({'error': 'El título es requerido y no puede estar vacío'}), 400
    if not data.get('client_name') or not str(data.get('client_name')).strip():
        return jsonify({'error': 'Título y nombre del cliente son requeridos'}), 400
    
    # --- Creación del objeto Ticket con todos los datos ---
    ticket = Ticket(
        title=data['title'],
        client_name=data['client_name'],
        description=data.get('description', ''),
        telephone_operator_name=data.get('telephone_operator_name', 'Operador Hardcodeado'),
        technician_name=data.get('technician_name', 'Técnico Hardcodeado'),
        unit_equipment_name=data.get('unit_equipment_name', 'Equipo Hardcodeado'),
        state=data.get('state', 'open'),
        service_record_description=data.get('service_record_description', 'Registro de servicio hardcodeado'),
        message_content=data.get('message_content', 'Mensaje hardcodeado')
    )
    
    db.session.add(ticket)
    db.session.commit()
    
    return jsonify(ticket.to_dict()), 201

@tickets_bp.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """
    @brief Obtiene un ticket específico por su ID.
    
    @param ticket_id El ID del ticket a obtener.
    
    @return Una respuesta JSON con los datos del ticket o un 404 si no se encuentra.
    ---
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

@tickets_bp.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    """
    @brief Actualiza un ticket existente.
    
    @details Recibe los campos a actualizar en formato JSON. Solo actualiza
             los campos permitidos y validados.
    
    @param ticket_id El ID del ticket a actualizar.
    
    @return Una respuesta JSON con el ticket actualizado o un 404 si no se encuentra.
    ---
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
        return jsonify({'error': 'No se proporcionaron datos'}), 400
    
    # --- Lógica de actualización segura y validada ---
    allowed_updates = {
        'title': lambda v: isinstance(v, str) and v.strip(),
        'description': lambda v: isinstance(v, str),
        'client_name': lambda v: isinstance(v, str) and v.strip(),
        'telephone_operator_name': lambda v: isinstance(v, str),
        'technician_name': lambda v: isinstance(v, str),
        'unit_equipment_name': lambda v: isinstance(v, str),
        'state': lambda v: v in {'open', 'in_progress', 'resolved', 'closed'},
        'service_record_description': lambda v: isinstance(v, str),
        'message_content': lambda v: isinstance(v, str)
    }
    
    for key, value in data.items():
        if key in allowed_updates:
            if allowed_updates[key](value):
                setattr(ticket, key, value.strip() if isinstance(value, str) else value)
            else:
                return jsonify({'error': f"Valor inválido para el campo '{key}'"}), 400
    
    db.session.commit()
    return jsonify(ticket.to_dict())

@tickets_bp.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    """
    @brief Elimina un ticket y sus incidentes asociados.
    
    @details Gracias a la configuración 'cascade' en el modelo, al eliminar
             un ticket, SQLAlchemy también elimina todos sus incidentes.
    
    @param ticket_id El ID del ticket a eliminar.
    
    @return Una respuesta JSON confirmando la eliminación o un 404 si no se encuentra.
    ---
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
    return jsonify({'message': 'Ticket eliminado exitosamente'})

# === NUEVOS ENDPOINTS PARA OPTIMIZACIÓN DEL TALLER ===

@tickets_bp.route('/tickets/<int:ticket_id>/optimal-workflow', methods=['GET'])
def get_optimal_workflow(ticket_id):
    """
    @brief Calcula y devuelve la ruta óptima para un ticket en el taller.
    
    @details Usa el algoritmo de Dijkstra para determinar el flujo óptimo
             de reparación basado en el tipo de equipo y los incidentes.
    
    @param ticket_id El ID del ticket a optimizar.
    
    @return Una respuesta JSON con la ruta óptima calculada.
    ---
    parameters:
      - in: path
        name: ticket_id
        required: true
        type: integer
        description: ID del ticket
    responses:
      200:
        description: Ruta óptima calculada exitosamente
        schema:
          type: object
          properties:
            ticket_id:
              type: integer
            title:
              type: string
            current_location:
              type: string
            recommended_next_step:
              type: string
            estimated_process_time:
              type: integer
            full_path:
              type: array
              items:
                type: string
            equipment:
              type: string
            client:
              type: string
      404:
        description: Ticket no encontrado
      500:
        description: Error en el cálculo de la ruta
    """
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        optimal_path = ticket.calculate_optimal_workflow()
        
        db.session.commit()
        
        return jsonify({
            'ticket_id': ticket_id,
            'title': ticket.title,
            'current_location': ticket.current_location,
            'recommended_next_step': ticket.recommended_next_step,
            'estimated_process_time': ticket.estimated_process_time,
            'full_path': optimal_path,
            'equipment': ticket.unit_equipment_name,
            'client': ticket.client_name
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tickets_bp.route('/tickets/<int:ticket_id>/move-to-next', methods=['POST'])
def move_to_next_step(ticket_id):
    """
    @brief Mueve el ticket al siguiente paso en el flujo de trabajo óptimo.
    
    @details Actualiza la ubicación actual del ticket y recalcula el siguiente
             paso recomendado usando el algoritmo de Dijkstra.
    
    @param ticket_id El ID del ticket a mover.
    
    @return Una respuesta JSON con la nueva ubicación y siguiente paso.
    ---
    parameters:
      - in: path
        name: ticket_id
        required: true
        type: integer
        description: ID del ticket
    responses:
      200:
        description: Ticket movido exitosamente
        schema:
          type: object
          properties:
            ticket_id:
              type: integer
            previous_location:
              type: string
            new_location:
              type: string
            next_recommended:
              type: string
            estimated_remaining_time:
              type: integer
            message:
              type: string
      400:
        description: El equipo ya está terminado
      404:
        description: Ticket no encontrado
      500:
        description: Error al procesar el movimiento
    """
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        
        if ticket.current_location == 'terminado':
            return jsonify({'error': 'El equipo ya está terminado'}), 400
        
        # Si no hay siguiente paso recomendado, calcularlo
        if not ticket.recommended_next_step:
            ticket.calculate_optimal_workflow()
        
        # Mover al siguiente paso
        previous_location = ticket.current_location
        ticket.current_location = ticket.recommended_next_step
        
        # Recalcular siguiente paso
        new_path = ticket.calculate_optimal_workflow()
        
        db.session.commit()
        
        return jsonify({
            'ticket_id': ticket_id,
            'previous_location': previous_location,
            'new_location': ticket.current_location,
            'next_recommended': ticket.recommended_next_step,
            'estimated_remaining_time': ticket.estimated_process_time,
            'message': f'Equipo movido de {previous_location} a {ticket.current_location}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tickets_bp.route('/tickets/active', methods=['GET'])
def get_active_tickets():
    """
    @brief Obtiene todos los tickets activos (no terminados).
    
    @details Filtra los tickets que no están en estado 'terminado' y
             son útiles para el monitoreo del taller.
    
    @return Una respuesta JSON con la lista de tickets activos.
    ---
    responses:
      200:
        description: Lista de tickets activos
        schema:
          type: object
          properties:
            active_tickets:
              type: array
              items:
                type: object
            count:
              type: integer
      500:
        description: Error al obtener tickets activos
    """
    try:
        active_tickets = Ticket.query.filter(Ticket.current_location != 'terminado').all()
        
        return jsonify({
            'active_tickets': [ticket.to_dict() for ticket in active_tickets],
            'count': len(active_tickets)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tickets_bp.route('/tickets/<int:ticket_id>/update-location', methods=['PUT'])
def update_ticket_location(ticket_id):
    """
    @brief Actualiza manualmente la ubicación de un ticket en el taller.
    
    @details Permite actualizar la ubicación actual de un equipo y
             recalcula automáticamente la ruta óptima desde esa nueva ubicación.
    
    @param ticket_id El ID del ticket a actualizar.
    
    @return Una respuesta JSON con la nueva ubicación y siguiente paso.
    ---
    parameters:
      - in: path
        name: ticket_id
        required: true
        type: integer
        description: ID del ticket
      - in: body
        name: location
        required: true
        schema:
          type: object
          required:
            - location
          properties:
            location:
              type: string
              description: Nueva ubicación del ticket
    responses:
      200:
        description: Ubicación actualizada exitosamente
      400:
        description: Ubicación no proporcionada
      404:
        description: Ticket no encontrado
      500:
        description: Error al actualizar la ubicación
    """
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        data = request.get_json()
        
        if 'location' not in data:
            return jsonify({'error': 'Ubicación no proporcionada'}), 400
        
        new_location = data['location']
        ticket.current_location = new_location
        
        # Recalcular ruta desde la nueva ubicación
        ticket.calculate_optimal_workflow()
        
        db.session.commit()
        
        return jsonify({
            'ticket_id': ticket_id,
            'new_location': ticket.current_location,
            'recommended_next_step': ticket.recommended_next_step,
            'message': f'Ubicación actualizada a {new_location}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tickets_bp.route('/tickets/batch-optimize', methods=['POST'])
def batch_optimize_workflows():
    """
    @brief Optimiza el flujo de trabajo para todos los tickets activos.
    
    @details Recalcula las rutas óptimas para todos los tickets que no
             están terminados, útil para reoptimizar después de cambios
             en la configuración del taller.
    
    @return Una respuesta JSON con el resultado de la optimización.
    ---
    responses:
      200:
        description: Optimización completada
        schema:
          type: object
          properties:
            optimized_tickets:
              type: integer
            message:
              type: string
      500:
        description: Error en la optimización
    """
    try:
        active_tickets = Ticket.query.filter(Ticket.current_location != 'terminado').all()
        optimized_count = 0
        
        for ticket in active_tickets:
            ticket.calculate_optimal_workflow()
            optimized_count += 1
        
        db.session.commit()
        
        return jsonify({
            'optimized_tickets': optimized_count,
            'message': f'Se optimizaron {optimized_count} tickets activos'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500