from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from routes import register_routes
from models import init_db, db

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for development
CORS(app)

# Initialize database
init_db(app)

# Initialize migration support
migrate = Migrate(app, db)

# Register API routes
register_routes(app)

@app.route('/api/status')
def status():
    return jsonify({"status": "ok", "message": "Health Connect API is running"})

if __name__ == '__main__':
    app.run(debug=True)