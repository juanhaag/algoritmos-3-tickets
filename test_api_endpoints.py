#!/usr/bin/env python3
"""
Pruebas completas de la API: tickets e incidents (CRUD + casos de error + filtros).
Ejecutar con la app en http://localhost:5000
"""

import requests
import sys
import time

API = "http://localhost:5000"
TMO = 5

def ok(resp, expected=200):
    code = resp.status_code if resp is not None else None
    ok = code == expected
    print(f"{resp.request.method} {resp.request.url} -> {code} (esperado {expected})", "OK" if ok else "FAIL")
    if not ok:
        try:
            print("Body:", resp.text)
        except Exception:
            pass
    return ok

def expect_fail(resp, expected_codes=(400,404)):
    code = resp.status_code if resp is not None else None
    okflag = code in expected_codes
    print(f"{resp.request.method} {resp.request.url} -> {code} (esperado uno de {expected_codes})", "OK" if okflag else "FAIL")
    if not okflag:
        print("Body:", resp.text)
    return okflag

def test_swagger_and_home():
    r = requests.get(f"{API}/", timeout=TMO)
    if not ok(r, 200): return False
    r = requests.get(f"{API}/swagger/", timeout=TMO)
    # swagger UI devuelve HTML (200). apispec.json debe ser JSON.
    ok(r, 200)
    r = requests.get(f"{API}/apispec.json", timeout=TMO)
    ok(r, 200)
    r = requests.get(f"{API}/cliente-prueba", timeout=TMO)
    ok(r, 200)
    return True

def test_tickets_crud():
    # crear ticket
    payload = {"title": "Prueba API", "client_name": "Cliente X", "description": "desc"}
    r = requests.post(f"{API}/tickets", json=payload, timeout=TMO)
    if not ok(r, 201): return False
    ticket = r.json()
    ticket_id = ticket.get("id")
    print("ticket_id =", ticket_id)
    if not ticket_id:
        print("No se devolvió id")
        return False

    # listar tickets
    r = requests.get(f"{API}/tickets", timeout=TMO)
    if not ok(r, 200): return False
    # obtener por id
    r = requests.get(f"{API}/tickets/{ticket_id}", timeout=TMO)
    if not ok(r, 200): return False

    # actualizar ticket
    update = {"title": "Prueba API - edit", "state": "in_progress"}
    r = requests.put(f"{API}/tickets/{ticket_id}", json=update, timeout=TMO)
    if not ok(r, 200): return False
    if r.json().get("title") != update["title"]:
        print("Update no aplicado correctamente"); return False

    # filtro por state (debe incluir el ticket actualizado)
    r = requests.get(f"{API}/tickets?state=in_progress", timeout=TMO)
    if not ok(r, 200): return False
    found = any(t.get("id") == ticket_id for t in r.json())
    print("Filtro state in_progress ->", "encontrado" if found else "no encontrado")
    if not found: return False

    return ticket_id

def test_incidents_crud(ticket_id):
    # intento crear incidente inválido (sin ticket_id)
    bad = {"description": "sin ticket"}
    r = requests.post(f"{API}/incidents", json=bad, timeout=TMO)
    if not expect_fail(r, (400,)): return False

    # crear incidente válido
    payload = {"description": "Incidente prueba", "ticket_id": ticket_id, "priority": "high"}
    r = requests.post(f"{API}/incidents", json=payload, timeout=TMO)
    if not ok(r, 201): return False
    incident = r.json()
    incident_id = incident.get("id")
    print("incident_id =", incident_id)
    if not incident_id: return False

    # listar incidentes
    r = requests.get(f"{API}/incidents", timeout=TMO)
    if not ok(r, 200): return False

    # listar incidentes filtrando por ticket_id
    r = requests.get(f"{API}/incidents?ticket_id={ticket_id}", timeout=TMO)
    if not ok(r, 200): return False
    found = any(i.get("id") == incident_id for i in r.json())
    print("Filtro incidents?ticket_id= ->", "encontrado" if found else "no encontrado")
    if not found: return False

    # obtener por id
    r = requests.get(f"{API}/incidents/{incident_id}", timeout=TMO)
    if not ok(r, 200): return False

    # actualizar incidente
    upd = {"status": "in_progress", "priority": "medium"}
    r = requests.put(f"{API}/incidents/{incident_id}", json=upd, timeout=TMO)
    if not ok(r, 200): return False
    if r.json().get("status") != "in_progress":
        print("Update incidente no aplicado"); return False

    # borrar incidente
    r = requests.delete(f"{API}/incidents/{incident_id}", timeout=TMO)
    if not ok(r, 200): return False

    # confirmar 404 al obtener eliminado
    r = requests.get(f"{API}/incidents/{incident_id}", timeout=TMO)
    if not expect_fail(r, (404,)): return False

    return True

def test_error_cases(ticket_id):
    # actualizar ticket inexistente
    r = requests.put(f"{API}/tickets/9999999", json={"title":"x"}, timeout=TMO)
    expect_fail(r, (404,))

    # borrar ticket inexistente
    r = requests.delete(f"{API}/tickets/9999999", timeout=TMO)
    expect_fail(r, (404,))

    # crear incidente con ticket inexistente
    r = requests.post(f"{API}/incidents", json={"description":"x","ticket_id":9999999}, timeout=TMO)
    expect_fail(r, (404,400))

def main():
    ok_all = True
    print("Comprobando servicios básicos...")
    ok_all &= test_swagger_and_home()

    print("\nRealizando CRUD tickets...")
    ticket_id = test_tickets_crud()
    if not ticket_id:
        print("Fallo en CRUD de tickets"); sys.exit(1)

    time.sleep(0.2)
    print("\nRealizando CRUD incidents asociados al ticket creado...")
    ok_all &= test_incidents_crud(ticket_id)

    print("\nProbando casos de error...")
    test_error_cases(ticket_id)

    # eliminar ticket creado (cleanup)
    print("\nEliminar ticket creado (cleanup)...")
    r = requests.delete(f"{API}/tickets/{ticket_id}", timeout=TMO)
    ok(r, 200)

    if ok_all:
        print("\nTodas las pruebas pasaron (o al menos los checks críticos).")
        return 0
    else:
        print("\nAlgunas pruebas fallaron.")
        return 2

if __name__ == "__main__":
    sys.exit(main())