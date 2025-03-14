from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from pathlib import Path

# Create database instance
db = SQLAlchemy()
migrate = Migrate()

def create_app(config=None):
    app = Flask(__name__)
    
    # Configure the app
    app_config = {
        'SECRET_KEY': os.environ.get('SECRET_KEY', 'dev-key-change-in-production'),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }
    
    # Create data directory if it doesn't exist
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)
    app_config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{data_dir}/health_connect.db'
    
    if config:
        app_config.update(config)
    
    app.config.update(app_config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.health_data import health_data_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(health_data_bp, url_prefix='/api')
    
    # Status endpoint
    @app.route('/api/status')
    def status():
        from flask import jsonify
        return jsonify({"status": "ok", "message": "Health Connect API is running"})
    
    return app