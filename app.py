# Root entry point — delegates to the backend Flask application.
# Run this file from the project root directory: python app.py
from backend.app import app

if __name__ == "__main__":
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
