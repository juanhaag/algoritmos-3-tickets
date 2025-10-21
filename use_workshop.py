# examples/uso_taller_simple.py
"""
Ejemplos de uso del sistema de optimización de taller (solo API)
"""

import requests
import time

BASE_URL = "http://localhost:5000"

def verificar_servidor():
    """Verifica si el servidor está ejecutándose"""
    print("🔍 Verificando servidor...")
    try:
        response = requests.get(f'{BASE_URL}/', timeout=5)
        if response.status_code == 200:
            print("✅ Servidor Flask está ejecutándose")
            return True
        else:
            print(f"❌ Servidor respondió con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Servidor NO está ejecutándose")
        print("💡 Ejecuta primero: python app.py")
        return False

def crear_ticket_ejemplo():
    """Crea un ticket de ejemplo usando la API"""
    print("\n📝 Creando ticket de ejemplo...")
    
    ticket_data = {
        "title": "Laptop Gaming - Problemas de rendimiento",
        "description": "Equipo se apaga repentinamente durante juegos",
        "client_name": "Carlos Rodríguez",
        "unit_equipment_name": "Laptop Gaming ASUS",
        "current_location": "recepcion"
    }
    
    try:
        response = requests.post(f'{BASE_URL}/tickets', json=ticket_data, timeout=10)
        if response.status_code == 201:
            ticket = response.json()
            print(f"✅ Ticket creado - ID: {ticket['id']}")
            return ticket['id']
        else:
            print(f"❌ Error creando ticket: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def simular_flujo_completo(ticket_id):
    """Simula el flujo completo de un ticket usando la API"""
    print(f"\n🔄 Simulando flujo para ticket {ticket_id}...")
    
    max_movimientos = 8
    movimientos = 0
    
    while movimientos < max_movimientos:
        # Obtener estado actual
        response = requests.get(f'{BASE_URL}/tickets/{ticket_id}', timeout=5)
        if response.status_code != 200:
            print(f"❌ Error obteniendo ticket: {response.status_code}")
            break
            
        ticket = response.json()
        ubicacion_actual = ticket.get('current_location', 'desconocido')
        
        print(f"\nPaso {movimientos + 1}:")
        print(f"  Ubicación: {ubicacion_actual}")
        print(f"  Siguiente: {ticket.get('recommended_next_step', 'N/A')}")
        print(f"  Tiempo: {ticket.get('estimated_process_time', 'N/A')} min")
        
        # Si ya está terminado, salir
        if ubicacion_actual == 'terminado':
            print("🎉 ¡Ticket completado!")
            break
        
        # Mover al siguiente paso
        response = requests.post(f'{BASE_URL}/tickets/{ticket_id}/move-to-next', timeout=5)
        if response.status_code == 200:
            resultado = response.json()
            print(f"  ✅ Movido a: {resultado['new_location']}")
        else:
            error = response.json().get('error', 'Error desconocido')
            print(f"  ❌ Error: {error}")
            break
        
        movimientos += 1
        time.sleep(1)  # Pequeña pausa para ver el flujo
    
    if movimientos >= max_movimientos:
        print("⚠️  Límite de movimientos alcanzado")

def optimizar_ticket(ticket_id):
    """Optimiza un ticket específico"""
    print(f"\n⚡ Optimizando ticket {ticket_id}...")
    
    try:
        response = requests.get(f'{BASE_URL}/tickets/{ticket_id}/optimal-workflow', timeout=10)
        if response.status_code == 200:
            resultado = response.json()
            print(f"✅ Ruta óptima calculada:")
            print(f"   Ruta: {' → '.join(resultado.get('full_path', []))}")
            print(f"   Siguiente: {resultado.get('recommended_next_step', 'N/A')}")
            print(f"   Tiempo: {resultado.get('estimated_process_time', 'N/A')} min")
        else:
            print(f"❌ Error optimizando: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def mostrar_tickets_activos():
    """Muestra todos los tickets activos"""
    print("\n📊 Tickets activos en el sistema:")
    
    try:
        response = requests.get(f'{BASE_URL}/tickets/active', timeout=5)
        if response.status_code == 200:
            datos = response.json()
            print(f"Total activos: {datos.get('count', 0)}")
            
            for ticket in datos.get('active_tickets', []):
                print(f"  - Ticket {ticket['id']}: {ticket['title']}")
                print(f"    Ubicación: {ticket.get('current_location', 'N/A')}")
                print(f"    Siguiente: {ticket.get('recommended_next_step', 'N/A')}")
                print(f"    Tiempo: {ticket.get('estimated_process_time', 'N/A')} min")
                print()
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("   SISTEMA DE OPTIMIZACIÓN - EJEMPLOS API")
    print("=" * 50)
    
    if not verificar_servidor():
        exit(1)
    
    # 1. Crear ticket de ejemplo
    ticket_id = crear_ticket_ejemplo()
    
    if ticket_id:
        # 2. Optimizar el ticket
        optimizar_ticket(ticket_id)
        
        # 3. Simular flujo completo
        simular_flujo_completo(ticket_id)
        
        # 4. Mostrar todos los tickets activos
        mostrar_tickets_activos()
        
        print("\n" + "=" * 50)
        print("🎉 EJEMPLOS COMPLETADOS EXITOSAMENTE")
        print("=" * 50)
    else:
        print("❌ No se pudo crear ticket de ejemplo")