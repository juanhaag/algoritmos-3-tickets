WorkshopGraph = {
    'recepcion': {'diagnostico': 5, 'almacen': 10, 'espera': 2},
    'diagnostico': {'recepcion': 5, 'reparacion_simple': 3, 'reparacion_compleja': 7, 'espera': 1},
    'reparacion_simple': {'diagnostico': 3, 'pruebas': 4, 'almacen': 8},
    'reparacion_compleja': {'diagnostico': 7, 'pruebas': 6, 'espera_repuestos': 15},
    'pruebas': {'reparacion_simple': 4, 'reparacion_compleja': 6, 'terminado': 3, 'diagnostico': 5},
    'almacen': {'recepcion': 10, 'reparacion_simple': 8},
    'espera_repuestos': {'reparacion_compleja': 1},
    'espera': {'recepcion': 2, 'diagnostico': 1},
    'terminado': {}
}

# Para compatibilidad
TALLER_GRAPH = WorkshopGraph

RepairType = {
    'simple': ['recepcion', 'diagnostico', 'reparacion_simple', 'pruebas', 'terminado'],
    'complex': ['recepcion', 'diagnostico', 'reparacion_compleja', 'pruebas', 'terminado'],
    'standard': ['recepcion', 'diagnostico', 'reparacion_simple', 'pruebas', 'terminado']
}