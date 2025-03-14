# Health Connect Dashboard - Backend

Flask backend for storing and retrieving health data.

## Setup

```bash
# Create and activate a virtual environment
cd backend
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run the development server
flask run --host=0.0.0.0 --port=5000