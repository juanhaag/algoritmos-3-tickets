from flask import Flask
from flasgger import Swagger
from flask import render_template
from Database.database import init_db
from Controllers.TicketController import tickets_bp
from Controllers.IncidentController import incidents_bp

app = Flask(__name__)

# Configurar Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            #"rule_filter": lambda rule: True,, descomentenla si quieren que se vea default con las rutas /pagina principal y /cliente-prueba
            "rule_filter": lambda rule: not (
                rule.rule in ["/", "/cliente-prueba", "/favicon.ico", "/apispec.json"]
                or rule.rule.startswith("/flasgger_static")
            ),
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/",
}

# Plantilla para solucionar problema de visualización de Swagger UI con versiones recientes de Flask/Werkzeug.
# Carga los assets desde un CDN (unpkg) en lugar de localmente.
SWAGGER_TEMPLATE = {
    "swagger_ui_bundle_js": "//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js",
    "swagger_ui_standalone_preset_js": "//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js",
    "jquery_js": "//unpkg.com/jquery@2.2.4/dist/jquery.min.js",
    "swagger_ui_css": "//unpkg.com/swagger-ui-dist@3/swagger-ui.css",
    "tags": [
        {"name": "Tickets", "description": "Operaciones CRUD sobre tickets"},
        {"name": "Incidents", "description": "Operaciones CRUD sobre incidentes"},
    ],
}

# Inicializar base de datos
init_db(app)

# Registrar blueprints ANTES de inicializar Swagger para que pueda descubrir los endpoints
app.register_blueprint(tickets_bp)
app.register_blueprint(incidents_bp)

# Ahora inicializamos Swagger
swagger = Swagger(app, config=swagger_config, template=SWAGGER_TEMPLATE)


@app.route("/")
def home():
    """Página principal
    ---
    responses:
      200:
        description: Mensaje de bienvenida
    """
    return {
        "message": "API REST Simplificada - Sistema de Tickets e Incidentes",
        "version": "1.0",
        "endpoints": {
            "tickets": "/tickets",
            "incidents": "/incidents",
            "swagger": "/swagger",
            "cliente_prueba": "/cliente-prueba",
        },
    }


@app.route("/cliente-prueba")
def cliente_prueba():
    """Cliente de prueba para la API
    ---
    responses:
      200:
        description: Interfaz web para probar la API
    """
    return render_template("cliente_prueba.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
