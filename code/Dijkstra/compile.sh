#!/bin/bash
echo "Compilando DLL de Dijkstra..."
g++ -shared -o dijkstra.so -fPIC dijkstra.cpp
echo "Compilación completada. Verifica que dijkstra.so se haya creado."