from flask import Blueprint, request, jsonify
from ..Repositories.TicketRepository import TicketRepository

tickets_bp = Blueprint('tickets', __name__)
repo = TicketRepository()


@tickets_bp.route('/tickets', methods=['GET'])
def list_tickets():
    tickets = repo.get_all()
    return jsonify(tickets)


@tickets_bp.route('/tickets', methods=['POST'])
def create_ticket():
    payload = request.get_json() or {}
    client = payload.get('client')
    incident = payload.get('incident')
    message = payload.get('message', '')
    ticket_id = repo.create(client=client, incident=incident, message=message)
    return jsonify({'id': ticket_id}), 201


@tickets_bp.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    t = repo.get_by_id(ticket_id)
    if not t:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(t)


@tickets_bp.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    payload = request.get_json() or {}
    updated = repo.update(ticket_id, **payload)
    if not updated:
        return jsonify({'error': 'Not found or no valid fields provided'}), 400
    return jsonify({'updated': True})


@tickets_bp.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    deleted = repo.delete(ticket_id)
    if not deleted:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'deleted': True})
