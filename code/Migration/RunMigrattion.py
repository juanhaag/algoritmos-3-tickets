# migrations/run_migration.py
import sys
import os
# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AddOptimalFields import add_optimization_fields

if __name__ == "__main__":
    print("Ejecutando migración de base de datos...")
    add_optimization_fields()
    print("Migración completada!")