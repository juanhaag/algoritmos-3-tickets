from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def init_db(app: Flask):
    """
    @brief Inicializa la base de datos y crea las tablas.
    
    @details Configura la URI de la base de datos y otras opciones de SQLAlchemy,
             asocia la instancia de la base de datos con la aplicación Flask y
             crea todas las tablas definidas en los modelos si no existen.
    
    @param app La instancia de la aplicación Flask.
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketing_simplified.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()