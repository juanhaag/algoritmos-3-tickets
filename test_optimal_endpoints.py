# tests/test_optimization_endpoints.py
import requests
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:5000/api"

def test_optimization_endpoints():
    """Prueba todos los nuevos endpoints de optimización"""
    
    print("🧪 Probando endpoints de optimización...\n")
    
    # 1. Primero crear un ticket de prueba
    print("1. Creando ticket de prueba...")
    ticket_data = {
        "title": "Laptop no enciende - Prueba Optimización",
        "description": "Equipo no da señal de vida, posible falla de fuente",
        "client_name": "Cliente Prueba Optimización",
        "current_location": "recepcion"
    }
    
    response = requests.post(f"{BASE_URL}/tickets", json=ticket_data)
    
    if response.status_code != 201:
        print(f"❌ Error creando ticket: {response.status_code} - {response.text}")
        return
    
    ticket = response.json()
    ticket_id = ticket['id']
    print(f"✅ Ticket creado - ID: {ticket_id}")
    
    # 2. Probar endpoint de optimal-workflow
    print(f"\n2. Probando optimal-workflow para ticket {ticket_id}...")
    response = requests.get(f"{BASE_URL}/tickets/{ticket_id}/optimal-workflow")
    
    if response.status_code == 200:
        workflow = response.json()
        print(f"✅ Ruta óptima calculada:")
        print(f"   - Ubicación actual: {workflow['current_location']}")
        print(f"   - Siguiente paso: {workflow['recommended_next_step']}")
        print(f"   - Tiempo estimado: {workflow['estimated_process_time']} min")
        print(f"   - Ruta completa: {' → '.join(workflow['full_path'])}")
    else:
        print(f"❌ Error en optimal-workflow: {response.status_code} - {response.text}")
    
    # 3. Probar movimiento al siguiente paso
    print(f"\n3. Probando move-to-next para ticket {ticket_id}...")
    response = requests.post(f"{BASE_URL}/tickets/{ticket_id}/move-to-next")
    
    if response.status_code == 200:
        move_result = response.json()
        print(f"✅ Movimiento exitoso:")
        print(f"   - De: {move_result['previous_location']}")
        print(f"   - A: {move_result['new_location']}")
        print(f"   - Siguiente: {move_result['next_recommended']}")
    else:
        print(f"❌ Error en move-to-next: {response.status_code} - {response.text}")
    
    # 4. Probar actualización manual de ubicación
    print(f"\n4. Probando update-location para ticket {ticket_id}...")
    update_data = {
        "location": "diagnostico"
    }
    response = requests.put(f"{BASE_URL}/tickets/{ticket_id}/update-location", json=update_data)
    
    if response.status_code == 200:
        update_result = response.json()
        print(f"✅ Ubicación actualizada: {update_result['new_location']}")
    else:
        print(f"❌ Error en update-location: {response.status_code} - {response.text}")
    
    # 5. Probar lista de tickets activos
    print(f"\n5. Probando lista de tickets activos...")
    response = requests.get(f"{BASE_URL}/tickets/active")
    
    if response.status_code == 200:
        active_tickets = response.json()
        print(f"✅ Tickets activos: {active_tickets['count']}")
        for ticket in active_tickets['active_tickets']:
            print(f"   - Ticket {ticket['id']}: {ticket['title']} ({ticket['current_location']})")
    else:
        print(f"❌ Error en active tickets: {response.status_code} - {response.text}")
    
    # 6. Probar optimización por lotes
    print(f"\n6. Probando batch-optimize...")
    response = requests.post(f"{BASE_URL}/tickets/batch-optimize")
    
    if response.status_code == 200:
        batch_result = response.json()
        print(f"✅ Optimización por lotes: {batch_result['message']}")
    else:
        print(f"❌ Error en batch-optimize: {response.status_code} - {response.text}")
    
    # 7. Verificar ticket actualizado
    print(f"\n7. Verificando estado final del ticket {ticket_id}...")
    response = requests.get(f"{BASE_URL}/tickets/{ticket_id}")
    
    if response.status_code == 200:
        final_ticket = response.json()
        print(f"✅ Estado final del ticket:")
        print(f"   - Ubicación: {final_ticket['current_location']}")
        print(f"   - Siguiente paso: {final_ticket['recommended_next_step']}")
        print(f"   - Tiempo estimado: {final_ticket['estimated_process_time']} min")
    else:
        print(f"❌ Error obteniendo ticket final: {response.status_code} - {response.text}")
    
    print(f"\n🎉 Pruebas completadas! Ticket de prueba ID: {ticket_id}")

def test_with_swagger():
    """Instrucciones para probar con Swagger UI"""
    print("\n📚 Para probar con Swagger UI:")
    print("1. Inicia tu servidor Flask")
    print("2. Ve a http://localhost:5000/apidocs/")
    print("3. Los nuevos endpoints estarán en el grupo 'tickets':")
    print("   - GET /tickets/{id}/optimal-workflow")
    print("   - POST /tickets/{id}/move-to-next") 
    print("   - PUT /tickets/{id}/update-location")
    print("   - GET /tickets/active")
    print("   - POST /tickets/batch-optimize")
    print("4. Usa el ticket ID creado en las pruebas: {ticket_id}")

if __name__ == "__main__":
    # Ejecutar pruebas automáticas
    test_optimization_endpoints()
    
    # Mostrar instrucciones Swagger
    test_with_swagger()