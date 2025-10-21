@echo off
echo ===============================================
echo   SISTEMA DE TICKETS E INCIDENTES - INICIO
echo ===============================================
echo.

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Iniciando la aplicacion...
echo.
echo La API estara disponible en:
echo   - API: http://localhost:5000
echo   - Swagger: http://localhost:5000/swagger  
echo   - Cliente de prueba: http://localhost:5000/cliente-prueba
echo.
echo Presiona Ctrl+C para detener la aplicacion
echo.

cd code
python app.py
