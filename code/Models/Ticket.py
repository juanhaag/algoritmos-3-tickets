from Database.database import db
from datetime import datetime
from typing import List, TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
import ctypes
import json
import os


if TYPE_CHECKING:
    from .Incident import Incident

class Ticket(db.Model):
    """
    @brief Modelo de datos para un Ticket.
    
    @details Representa un ticket de soporte que agrupa uno o más incidentes.
             Para fines educativos, muchos de sus campos son hardcodeados.
    """
    __tablename__ = 'tickets'
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(db.Text, nullable=True)
    
    # Campos hardcodeados según el diagrama UML
    client_name: Mapped[str] = mapped_column(db.String(100), nullable=False)  # Cliente hardcodeado
    telephone_operator_name: Mapped[Optional[str]] = mapped_column(db.String(100), default='Operador Hardcodeado')  # TelephoneOperator hardcodeado
    technician_name: Mapped[Optional[str]] = mapped_column(db.String(100), default='Técnico Hardcodeado')  # Technician hardcodeado
    unit_equipment_name: Mapped[Optional[str]] = mapped_column(db.String(100), default='Equipo Hardcodeado')  # UnitEquipment hardcodeado
    state: Mapped[Optional[str]] = mapped_column(db.String(50), default='open')  # State hardcodeado
    service_record_description: Mapped[Optional[str]] = mapped_column(db.Text, default='Registro de servicio hardcodeado', nullable=True)  # ServiceRecord hardcodeado
    message_content: Mapped[Optional[str]] = mapped_column(db.Text, default='Mensaje hardcodeado', nullable=True)  # Message hardcodeado
    
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación 1:N con Incident
    incidents: Mapped[List["Incident"]] = relationship(backref='ticket', lazy=True, cascade='all, delete-orphan')

    #Optimizacio Interna
    current_location = db.Column(db.String(50), default='recepcion')  # Ubicación actual del equipo
    recommended_next_step = db.Column(db.String(50))  # Siguiente paso recomendado
    estimated_process_time = db.Column(db.Integer)  # Tiempo estimado en minutos

    def __init__(self, title, client_name, description=None, 
                 telephone_operator_name=None, technician_name=None, 
                 unit_equipment_name=None, state=None, 
                 service_record_description=None, message_content=None,
                 current_location ='recepcion'):
        """
        @brief Constructor explícito para la clase Ticket.
        
        @details Este constructor se define para compatibilidad con herramientas de
                 análisis estático como Pylance, que no detectan el __init__
                 automático de SQLAlchemy.
        """
        self.title = title
        self.client_name = client_name
        self.description = description
        self.telephone_operator_name = telephone_operator_name
        self.technician_name = technician_name
        self.unit_equipment_name = unit_equipment_name
        self.state = state
        self.service_record_description = service_record_description
        self.message_content = message_content
        self.current_location = current_location

    def to_dict(self):
        """
        @brief Convierte el objeto Ticket a un diccionario.
        
        @details Serializa el ticket y su lista de incidentes asociados,
                 lo que es ideal para las respuestas de la API.
        
        @return Un diccionario que representa el ticket y sus incidentes.
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'client_name': self.client_name,
            'telephone_operator_name': self.telephone_operator_name,
            'technician_name': self.technician_name,
            'unit_equipment_name': self.unit_equipment_name,
            'state': self.state,
            'service_record_description': self.service_record_description,
            'message_content': self.message_content,
            'current_location': self.current_location,
            'recommended_next_step': self.recommended_next_step,
            'estimated_process_time': self.estimated_process_time,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'incidents': [incident.to_dict() for incident in self.incidents]
        }
    
    def __repr__(self):
        return f'<Ticket {self.id}: {self.title}>'
    
    def calculate_optimal_workflow(self):
        """
        @brief Calcula la ruta óptima para el proceso de reparación.
        
        @details Usa el algoritmo de Dijkstra para determinar el flujo más eficiente
                 a través del taller basado en el tipo de reparación necesaria.
        
        @return Lista con la ruta óptima de ubicaciones.
        """
        # Determinar tipo de reparación basado en incidentes
        repair_type = self._determine_repair_type()
        
        # Usar DLL de Dijkstra para calcular ruta óptima
        optimal_path = self._calculate_optimal_path_dll(self.current_location, 'terminado', repair_type)
        
        # Actualizar campos del ticket
        self.recommended_next_step = optimal_path[1] if len(optimal_path) > 1 else 'terminado'
        self.estimated_process_time = self._calculate_total_time(optimal_path, repair_type)
        
        return optimal_path
    
    def _determine_repair_type(self):
        """
        @brief Determina el tipo de reparación basado en los incidentes.
        
        @details Analiza las prioridades y descripciones de los incidentes
                 para clasificar la reparación como simple, compleja o estándar.
        
        @return String con el tipo de reparación ('simple', 'complex', 'standard')
        """
        if not self.incidents:
            return 'standard'
        
        priorities = [incident.priority for incident in self.incidents]
        descriptions = ' '.join([incident.description.lower() for incident in self.incidents])
        
        # Lógica para determinar complejidad
        if any(priority == 'high' for priority in priorities):
            return 'complex'
        elif 'complej' in descriptions or 'difícil' in descriptions or 'grave' in descriptions:
            return 'complex'
        elif any(priority == 'low' for priority in priorities):
            return 'simple'
        elif 'simple' in descriptions or 'sencill' in descriptions or 'leve' in descriptions:
            return 'simple'
        else:
            return 'standard'
    
    def _get_taller_graph(self):
        """
        @brief Define la estructura del taller como grafo para Dijkstra.
        """
        from Config.WorkshopLayout import WorkshopGraph  # Importar del archivo de configuración
        return WorkshopGraph
    
    def _calculate_optimal_path_python(self, start, end, repair_type):
        """
        @brief Implementación de respaldo de Dijkstra en Python.
        """
        graph = self._adapt_graph_for_repair_type(repair_type)
        
        # Implementación simple de Dijkstra
        distances = {node: float('inf') for node in graph}
        previous = {node: None for node in graph}
        distances[start] = 0
        
        nodes = set(graph.keys())
        
        while nodes:
            current = min(nodes, key=lambda node: distances[node])
            nodes.remove(current)
            
            if distances[current] == float('inf'):
                break
                
            for neighbor, weight in graph.get(current, {}).items():
                new_distance = distances[current] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current
        
        # Reconstruir el camino
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
        
        path.reverse()
        
        # Si no hay camino válido, devolver camino por defecto
        if not path or path[0] != start:
            path = [start, 'diagnostico', 'pruebas', 'terminado']  # Asegurar nombres en español
        
        print(f"🔄 Python Dijkstra devolvió: {path}")
        return path
    
    def _adapt_graph_for_repair_type(self, repair_type):
        """
        @brief Adapta el grafo del taller según el tipo de reparación.
        
        @details Modifica los pesos de las aristas para priorizar ciertas rutas
                según la complejidad de la reparación.
        
        @param repair_type Tipo de reparación ('simple', 'complex', 'standard')
        @return Grafo adaptado para el tipo de reparación
        """
        graph = self._get_taller_graph()
        
        if repair_type == 'simple':
            # Priorizar ruta simple: reducir tiempos en reparación simple
            if 'reparacion_simple' in graph and 'pruebas' in graph['reparacion_simple']:
                graph['reparacion_simple']['pruebas'] = 2  # Más rápido
        elif repair_type == 'complex':
            # Priorizar ruta compleja: reducir tiempos en reparación compleja
            if 'reparacion_compleja' in graph and 'pruebas' in graph['reparacion_compleja']:
                graph['reparacion_compleja']['pruebas'] = 4  # Más rápido
        
        return graph
    
    def _calculate_optimal_path_dll(self, start, end, repair_type):
        """Usa la DLL de Dijkstra para calcular ruta óptima"""
        try:
            # Ruta correcta a la DLL
            dll_path = os.path.join(os.path.dirname(__file__), '..', 'Dijkstra', 'dijkstra.dll')
            dll_path = os.path.abspath(dll_path)
            
            print(f"🔍 Buscando DLL en: {dll_path}")
            
            # Verificar si el archivo existe
            if not os.path.exists(dll_path):
                raise FileNotFoundError(f"No se encuentra la DLL en: {dll_path}")
            
            # Cargar DLL con ruta absoluta
            dijkstra = ctypes.CDLL(dll_path)
            
            # Configurar función (versión simplificada)
            dijkstra.calculate_optimal_path.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
            dijkstra.calculate_optimal_path.restype = ctypes.c_char_p
            
            # Llamar función
            start_bytes = start.encode('utf-8')
            end_bytes = end.encode('utf-8')
            
            result_ptr = dijkstra.calculate_optimal_path(start_bytes, end_bytes)
            
            if result_ptr:
                result_str = ctypes.string_at(result_ptr).decode('utf-8')
                # Liberar memoria si la DLL tiene esa función
                if hasattr(dijkstra, 'free_result'):
                    dijkstra.free_result(result_ptr)
                return json.loads(result_str)
            else:
                raise Exception("La DLL no devolvió resultado")
                
        except (OSError, AttributeError, FileNotFoundError, Exception) as e:
            print(f"❌ Error al usar DLL de Dijkstra: {e}")
            print("🔄 Usando implementación de respaldo en Python...")
            return self._calculate_optimal_path_python(start, end, repair_type)
        
    def _convert_graph_to_c_format(self, graph):
        """
        @brief Convierte el grafo de Python a formato compatible con C++.
        
        @details Esta función necesita ser adaptada según la implementación
                 específica de tu DLL de Dijkstra.
        
        @param graph Grafo en formato de diccionario de Python
        @return Puntero a estructura de datos compatible con C++
        """
        # Esta implementación depende de cómo esté diseñada tu DLL
        # Por ahora, devolvemos None y manejamos el error en la función principal
        return None
    
    def _calculate_total_time(self, path, repair_type):
        """
        @brief Calcula el tiempo total estimado para la ruta óptima.
        
        @param path Lista de ubicaciones en la ruta óptima
        @param repair_type Tipo de reparación
        @return Tiempo total estimado en minutos
        """
        graph = self._adapt_graph_for_repair_type(repair_type)
        total_time = 0
        
        for i in range(len(path) - 1):
            current = path[i]
            next_node = path[i + 1]
            if next_node in graph.get(current, {}):
                total_time += graph[current][next_node]
        
        return total_time
    
    def move_to_next_location(self):
        """
        @brief Mueve el ticket a la siguiente ubicación recomendada.
        
        @details Actualiza la ubicación actual y recalcula el siguiente paso.
        
        @return Tupla (ubicación_anterior, nueva_ubicación)
        """
        if not self.recommended_next_step:
            self.calculate_optimal_workflow()
        
        if self.recommended_next_step and self.recommended_next_step != 'terminado':
            previous_location = self.current_location
            self.current_location = self.recommended_next_step
            self.calculate_optimal_workflow()  # Recalcular siguiente paso
            return previous_location, self.current_location
        
        return self.current_location, self.current_location  # Ya terminado