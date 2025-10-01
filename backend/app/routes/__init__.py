# app/routes/__init__.py
from .auth_routes import auth_bp
from .phq9_routes import phq9_bp
# from .dashboard_routes import dashboard_bp  # if you have this

def register_routes(app):
    """Register all blueprints here"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(phq9_bp)
    # app.register_blueprint(dashboard_bp)  # optional
