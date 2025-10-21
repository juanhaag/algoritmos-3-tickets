@echo off
echo Compilando DLL de Dijkstra...
g++ -shared -o Dijkstra.dll -fPIC Dijkstra.cpp -std=c++11
echo Compilacion completada. Verifica que Dijkstra.dll se haya creado.
dir Dijkstra.dll
pause