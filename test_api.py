#!/usr/bin/env python3
"""
Script de prueba para verificar la API REST de Tickets e Incidentes
"""

import requests
import json
import time

API_BASE = "http://localhost:5000"

def test_api():
    """Ejecuta pruebas básicas de la API"""
    print("Iniciando pruebas de la API...")
    
    # Test 1: Verificar que la API está funcionando
    print("\n1. Verificando estado de la API...")
    try:
        response = requests.get(f"{API_BASE}/")
        if response.status_code == 200:
            print("La API está funcionando correctamente.")
            print(f"Respuesta: {response.json()}")
        else:
            print(f"Error en la API. Código de respuesta: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("No se puede conectar a la API. Asegúrese de que esté ejecutándose.")
        return False
    
    # Test 2: Crear un ticket
    print("\n2. Creando un ticket de prueba...")
    ticket_data = {
        "title": "Ticket de Prueba",
        "description": "Este es un ticket creado para probar la API",
        "client_name": "Cliente de Prueba",
        "telephone_operator_name": "Operador de Prueba",
        "technician_name": "Técnico de Prueba",
        "unit_equipment_name": "Equipo de Prueba",
        "state": "open",
        "service_record_description": "Registro de servicio de prueba",
        "message_content": "Mensaje de prueba"
    }
    
    try:
        response = requests.post(f"{API_BASE}/tickets", json=ticket_data)
        if response.status_code == 201:
            ticket = response.json()
            ticket_id = ticket['id']
            print(f"Ticket creado con éxito. ID: {ticket_id}")
        else:
            print(f"Error al crear el ticket. Código de respuesta: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"Error durante la creación del ticket: {e}")
        return False
    
    # Test 3: Crear un incidente para el ticket
    print("\n3. Creando un incidente para el ticket...")
    incident_data = {
        "description": "Error crítico en el sistema de autenticación",
        "priority": "high",
        "status": "open",
        "ticket_id": ticket_id
    }
    
    try:
        response = requests.post(f"{API_BASE}/incidents", json=incident_data)
        if response.status_code == 201:
            incident = response.json()
            incident_id = incident['id']
            print(f"Incidente creado con éxito. ID: {incident_id}")
        else:
            print(f"Error al crear el incidente. Código de respuesta: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"Error durante la creación del incidente: {e}")
        return False
    
    # Test 4: Obtener el ticket con sus incidentes
    print("\n4. Obteniendo ticket con sus incidentes...")
    try:
        response = requests.get(f"{API_BASE}/tickets/{ticket_id}")
        if response.status_code == 200:
            ticket_with_incidents = response.json()
            print("Ticket obtenido correctamente.")
            print(f"Título: {ticket_with_incidents['title']}")
            print(f"Cliente: {ticket_with_incidents['client_name']}")
            print(f"Número de incidentes: {len(ticket_with_incidents['incidents'])}")
        else:
            print(f"Error al obtener el ticket. Código de respuesta: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error al obtener el ticket: {e}")
        return False
    
    # Test 5: Listar todos los tickets
    print("\n5. Listando todos los tickets...")
    try:
        response = requests.get(f"{API_BASE}/tickets")
        if response.status_code == 200:
            tickets = response.json()
            print(f"Se encontraron {len(tickets)} tickets.")
        else:
            print(f"Error al listar los tickets. Código de respuesta: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error al listar los tickets: {e}")
        return False
    
    # Test 6: Listar incidentes filtrados por ticket
    print("\n6. Listando incidentes asociados al ticket...")
    try:
        response = requests.get(f"{API_BASE}/incidents?ticket_id={ticket_id}")
        if response.status_code == 200:
            incidents = response.json()
            print(f"Se encontraron {len(incidents)} incidentes para el ticket {ticket_id}.")
        else:
            print(f"Error al listar los incidentes. Código de respuesta: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error al listar los incidentes: {e}")
        return False
    
    # Test 7: Actualizar el estado del incidente
    print("\n7. Actualizando estado del incidente...")
    update_data = {
        "status": "in_progress",
        "priority": "medium"
    }
    
    try:
        response = requests.put(f"{API_BASE}/incidents/{incident_id}", json=update_data)
        if response.status_code == 200:
            updated_incident = response.json()
            print("Incidente actualizado correctamente.")
            print(f"Nuevo estado: {updated_incident['status']}")
            print(f"Nueva prioridad: {updated_incident['priority']}")
        else:
            print(f"Error al actualizar el incidente. Código de respuesta: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error al actualizar el incidente: {e}")
        return False
    
    print("\nTodas las pruebas se completaron con éxito.")
    print("\nResumen:")
    print(f" - Ticket creado: ID {ticket_id}")
    print(f" - Incidente creado: ID {incident_id}")
    print(" - Relación 1:N funcionando correctamente")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Sistema de Tickets e Incidentes - Pruebas de API")
    print("=" * 60)
    
    success = test_api()
    
    if success:
        print("\nEl sistema está funcionando correctamente.")
        print("Se puede probar también:")
        print(f" - Swagger UI: {API_BASE}/swagger")
        print(f" - Cliente web de prueba: {API_BASE}/cliente-prueba")
    else:
        print("\nAlgunas pruebas fallaron.")
        print("Verifique que la aplicación esté ejecutándose en http://localhost:5000")
