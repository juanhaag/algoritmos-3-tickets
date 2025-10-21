import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from Database.database import db
from sqlalchemy import text  # Importar text para consultas SQL

def add_optimization_fields():
    """Agrega los nuevos campos de optimización a la tabla tickets"""
    
    with app.app_context():
        try:
            print("🔄 Iniciando migración de base de datos...")
            
            # Verificar si las columnas ya existen
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('tickets')]
            
            print(f"Columnas actuales: {columns}")
            
            # Agregar columnas si no existen
            if 'current_location' not in columns:
                print("Agregando columna 'current_location'...")
                db.session.execute(text("""
                    ALTER TABLE tickets 
                    ADD COLUMN current_location VARCHAR(50) DEFAULT 'recepcion'
                """))
            
            if 'recommended_next_step' not in columns:
                print("Agregando columna 'recommended_next_step'...")
                db.session.execute(text("""
                    ALTER TABLE tickets 
                    ADD COLUMN recommended_next_step VARCHAR(50)
                """))
            
            if 'estimated_process_time' not in columns:
                print("Agregando columna 'estimated_process_time'...")
                db.session.execute(text("""
                    ALTER TABLE tickets 
                    ADD COLUMN estimated_process_time INTEGER
                """))
            
            db.session.commit()
            print("✅ Migración completada exitosamente")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error en migración: {e}")
            
            # Método alternativo para SQLite
            if "ALTER" in str(e) or "SQLite" in str(e):
                print("Intentando método alternativo para SQLite...")
                migrate_sqlite()

def migrate_sqlite():
    """Método alternativo para SQLite que no soporta bien ALTER TABLE"""
    try:
        print("🔄 Usando método SQLite (recrear tabla)...")
        
        # 1. Crear nueva tabla con las columnas adicionales
        db.session.execute(text("""
            CREATE TABLE tickets_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                client_name VARCHAR(100) NOT NULL,
                telephone_operator_name VARCHAR(100) DEFAULT 'Operador Hardcodeado',
                technician_name VARCHAR(100) DEFAULT 'Técnico Hardcodeado',
                unit_equipment_name VARCHAR(100) DEFAULT 'Equipo Hardcodeado',
                state VARCHAR(50) DEFAULT 'open',
                service_record_description TEXT DEFAULT 'Registro de servicio hardcodeado',
                message_content TEXT DEFAULT 'Mensaje hardcodeado',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                current_location VARCHAR(50) DEFAULT 'recepcion',
                recommended_next_step VARCHAR(50),
                estimated_process_time INTEGER
            )
        """))
        
        # 2. Copiar datos de la tabla vieja
        db.session.execute(text("""
            INSERT INTO tickets_new (
                id, title, description, client_name, telephone_operator_name,
                technician_name, unit_equipment_name, state, service_record_description,
                message_content, created_at, updated_at, current_location
            )
            SELECT 
                id, title, description, client_name, telephone_operator_name,
                technician_name, unit_equipment_name, state, service_record_description,
                message_content, created_at, updated_at, 'recepcion'
            FROM tickets
        """))
        
        # 3. Eliminar tabla vieja y renombrar nueva
        db.session.execute(text("DROP TABLE tickets"))
        db.session.execute(text("ALTER TABLE tickets_new RENAME TO tickets"))
        
        db.session.commit()
        print("✅ Migración SQLite completada exitosamente")
        
    except Exception as e2:
        db.session.rollback()
        print(f"❌ Error crítico en migración SQLite: {e2}")

if __name__ == "__main__":
    add_optimization_fields()