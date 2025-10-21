#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <queue>
#include <limits>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <cstring>

using namespace std;

extern "C" {

    // Estructura para representar el grafo
    struct Graph {
        map<string, map<string, int>> adjacencyList;
    };

    // Función auxiliar para convertir string a graph
    Graph* parseGraph(const char* graphStr) {
        // Para simplificar, usaremos un grafo predefinido
        // En una implementación real, parsearías el string JSON
        Graph* graph = new Graph();
        
        // Grafo hardcodeado del taller (mismo que en Python)
        graph->adjacencyList["recepcion"]["diagnostico"] = 5;
        graph->adjacencyList["recepcion"]["almacen"] = 10;
        graph->adjacencyList["recepcion"]["espera"] = 2;
        
        graph->adjacencyList["diagnostico"]["recepcion"] = 5;
        graph->adjacencyList["diagnostico"]["reparacion_simple"] = 3;
        graph->adjacencyList["diagnostico"]["reparacion_compleja"] = 7;
        graph->adjacencyList["diagnostico"]["espera"] = 1;
        
        graph->adjacencyList["reparacion_simple"]["diagnostico"] = 3;
        graph->adjacencyList["reparacion_simple"]["pruebas"] = 4;
        graph->adjacencyList["reparacion_simple"]["almacen"] = 8;
        
        graph->adjacencyList["reparacion_compleja"]["diagnostico"] = 7;
        graph->adjacencyList["reparacion_compleja"]["pruebas"] = 6;
        graph->adjacencyList["reparacion_compleja"]["espera_repuestos"] = 15;
        
        graph->adjacencyList["pruebas"]["reparacion_simple"] = 4;
        graph->adjacencyList["pruebas"]["reparacion_compleja"] = 6;
        graph->adjacencyList["pruebas"]["terminado"] = 3;
        graph->adjacencyList["pruebas"]["diagnostico"] = 5;
        
        graph->adjacencyList["almacen"]["recepcion"] = 10;
        graph->adjacencyList["almacen"]["reparacion_simple"] = 8;
        
        graph->adjacencyList["espera_repuestos"]["reparacion_compleja"] = 1;
        
        graph->adjacencyList["espera"]["recepcion"] = 2;
        graph->adjacencyList["espera"]["diagnostico"] = 1;
        
        return graph;
    }

    // Función para liberar memoria del grafo
    void freeGraph(Graph* graph) {
        delete graph;
    }

    // Implementación del algoritmo de Dijkstra
    const char* calculate_optimal_path(const char* start, const char* end, void* graphPtr) {
        Graph* graph = static_cast<Graph*>(graphPtr);
        
        string startStr(start);
        string endStr(end);
        
        // Verificar que los nodos existan en el grafo
        if (graph->adjacencyList.find(startStr) == graph->adjacencyList.end() ||
            graph->adjacencyList.find(endStr) == graph->adjacencyList.end()) {
            return "[]";
        }
        
        // Estructuras para Dijkstra
        map<string, int> distances;
        map<string, string> previous;
        priority_queue<pair<int, string>, 
                          vector<pair<int, string>>, 
                          greater<pair<int, string>>> pq;
        
        // Inicializar distancias
        for (const auto& node : graph->adjacencyList) {
            distances[node.first] = numeric_limits<int>::max();
        }
        distances[startStr] = 0;
        pq.push({0, startStr});
        
        // Algoritmo de Dijkstra
        while (!pq.empty()) {
            string current = pq.top().second;
            int currentDist = pq.top().first;
            pq.pop();
            
            if (currentDist > distances[current]) {
                continue;
            }
            
            // Si llegamos al destino, podemos terminar
            if (current == endStr) {
                break;
            }
            
            // Explorar vecinos
            for (const auto& neighbor : graph->adjacencyList[current]) {
                string nextNode = neighbor.first;
                int weight = neighbor.second;
                int newDist = currentDist + weight;
                
                if (newDist < distances[nextNode]) {
                    distances[nextNode] = newDist;
                    previous[nextNode] = current;
                    pq.push({newDist, nextNode});
                }
            }
        }
        
        // Reconstruir el camino
        vector<string> path;
        string current = endStr;
        
        while (!current.empty() && previous.find(current) != previous.end()) {
            path.push_back(current);
            current = previous[current];
        }
        path.push_back(startStr);
        
        // Invertir el camino
        reverse(path.begin(), path.end());
        
        // Convertir a JSON string
        stringstream json;
        json << "[";
        for (size_t i = 0; i < path.size(); ++i) {
            json << "\"" << path[i] << "\"";
            if (i < path.size() - 1) {
                json << ",";
            }
        }
        json << "]";
        
        // Devolver como C string (Python se encargará de liberar la memoria)
        char* result = new char[json.str().length() + 1];
        strcpy(result, json.str().c_str());
        
        return result;
    }

    // Función wrapper que Python llamará
    const char* calculate_optimal_path_wrapper(const char* start, const char* end, void* graphPtr) {
        return calculate_optimal_path(start, end, graphPtr);
    }
}