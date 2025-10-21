# Sistema de Tickets e Incidentes - API REST Simplificada

## 📋 Descripción

Sistema simplificado de gestión de tickets e incidentes implementado con Python, Flask, SQLite y SQLAlchemy. Cumple con el requisito de mantener una relación 1:N entre Tickets e Incidentes, mientras que el resto de las entidades se simulan con campos "hardcodeados" para fines educativos.

## 🚀 Características

- **Modelos SQLAlchemy**: `Ticket` e `Incident` implementados con la sintaxis moderna de SQLAlchemy 2.0.
- **Relación 1:N**: Un ticket puede tener múltiples incidentes. La eliminación de un ticket elimina en cascada sus incidentes asociados.
- **API REST completa**: Endpoints CRUD (Crear, Leer, Actualizar, Eliminar) para `Tickets` e `Incidentes`.
- **Documentación Interactiva**: Interfaz de Swagger UI disponible en `/swagger` para probar la API desde el navegador.
- **Cliente de Prueba**: Una sencilla interfaz web en `/cliente-prueba` para interactuar con la API.
- **Scripts de Inicio**: `iniciar.bat` (Windows) y `iniciar.sh` (Linux/macOS) para instalar dependencias y ejecutar la aplicación con un solo comando.
- **Pruebas Automatizadas**: Un script `test_api.py` que verifica el funcionamiento de todos los endpoints.

## 🛠️ Uso

El proyecto incluye scripts para facilitar su ejecución en diferentes sistemas operativos. Estos scripts se encargan de instalar las dependencias y lanzar la aplicación.

- **En Windows**:
  ```bash
  .\iniciar.bat
  ```

- **En Linux o macOS**:
  ```bash
  chmod +x iniciar.sh
  ./iniciar.sh
  ```

3. **Acceder a la aplicación**:
   - API: `http://localhost:5000`
   - Swagger: `http://localhost:5000/swagger`
   - Cliente de prueba: `http://localhost:5000/cliente-prueba`

## 📊 Estructura de la Base de Datos

### Tabla `tickets`
- `id`: Clave primaria
- `title`: Título del ticket
- `description`: Descripción del problema
- `client_name`: Nombre del cliente (hardcodeado)
- `telephone_operator_name`: Nombre del operador telefónico (hardcodeado)
- `technician_name`: Nombre del técnico (hardcodeado)
- `unit_equipment_name`: Nombre del equipo (hardcodeado)
- `state`: Estado del ticket (hardcodeado)
- `service_record_description`: Descripción del registro de servicio (hardcodeado)
- `message_content`: Contenido del mensaje (hardcodeado)
- `created_at`: Fecha de creación
- `updated_at`: Fecha de última actualización

### Tabla `incidents`
- `id`: Clave primaria
- `description`: Descripción del incidente
- `priority`: Prioridad (low, medium, high)
- `status`: Estado (open, in_progress, resolved, closed)
- `ticket_id`: Clave foránea hacia tickets
- `created_at`: Fecha de creación
- `updated_at`: Fecha de última actualización

## 🔗 Endpoints de la API

### Tickets

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/tickets` | Listar todos los tickets |
| POST | `/tickets` | Crear nuevo ticket |
| GET | `/tickets/{id}` | Obtener ticket por ID |
| PUT | `/tickets/{id}` | Actualizar ticket |
| DELETE | `/tickets/{id}` | Eliminar ticket |

### Incidentes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/incidents` | Listar todos los incidentes |
| GET | `/incidents?ticket_id={id}` | Filtrar incidentes por ticket |
| POST | `/incidents` | Crear nuevo incidente |
| GET | `/incidents/{id}` | Obtener incidente por ID |
| PUT | `/incidents/{id}` | Actualizar incidente |
| DELETE | `/incidents/{id}` | Eliminar incidente |

## 📝 Ejemplos de Uso

### Crear un Ticket
```bash
curl -X POST http://localhost:5000/tickets \
     -H "Content-Type: application/json" \
     -d '{
       "title": "El sistema de facturación no responde",
       "client_name": "Cliente Principal S.A."
     }'
```

### Crear un Incidente
```bash
curl -X POST http://localhost:5000/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Error 500 en el módulo de usuarios",
    "priority": "high",
    "status": "open",
    "ticket_id": 1
  }'
```

### Obtener Tickets con sus Incidentes
```bash
curl http://localhost:5000/tickets
```

## 🧪 Pruebas

1. **Con Swagger**: Visita `/swagger` para probar la API interactivamente
2. **Con Cliente Web**: Visita `/cliente-prueba` para usar la interfaz web
3. **Con cURL**: Usa los ejemplos de arriba

## 📁 Estructura del Proyecto

```
code/
├── app.py                          # Aplicación principal
├── requirements.txt                # Dependencias
├── Database/
│   └── database.py                # Configuración SQLAlchemy
├── Models/
│   ├── Ticket.py                  # Modelo Ticket
│   └── Incident.py                # Modelo Incident
├── Controllers/
│   ├── TicketController.py        # Controlador REST Tickets
│   └── IncidentController.py      # Controlador REST Incidentes
└── templates/
    └── cliente_prueba.html        # Cliente web de prueba
```

## 🎯 Objetivos Educativos

Este proyecto demuestra:
- Uso de Flask para APIs REST
- Integración con SQLAlchemy ORM
- Relaciones 1:N entre modelos
- Documentación automática con Swagger
- Interfaz de cliente para pruebas
- Estructura MVC simplificada

## 🔧 Personalización

Para agregar más funcionalidades:
1. Modifica los modelos en `Models/`
2. Actualiza los controladores en `Controllers/`
3. Agrega nuevas rutas en `app.py`
4. Actualiza la documentación Swagger

---
