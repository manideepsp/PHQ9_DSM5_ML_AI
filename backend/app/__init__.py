from flask import Flask
from flask_cors import CORS
from .db import init_db, engine

def create_app():
    app = Flask(__name__)

    # DB init
    init_db(app)

    # Register Blueprints
    from .routes import register_routes
    register_routes(app)

    # CORS
    CORS(
        app,
        origins=["http://localhost:3000", "http://localhost:5173"],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        expose_headers=["Content-Type", "Authorization"]
    )

    return app
