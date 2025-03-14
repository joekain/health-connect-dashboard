def register_routes(app):
    from routes.health_data import health_data_bp
    from routes.auth import auth_bp
    
    app.register_blueprint(health_data_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')