from flask import Flask
import os
import logging
from config import config
from ml_utils import MLModelManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    # Initialize ML manager with error handling
    app.ml_manager = MLModelManager()
    
    # Try to load models, but don't crash if they fail
    try:
        success = app.ml_manager.load_models()
        if not success:
            print("⚠️ ML models failed to load - app will run without predictions")
    except Exception as e:
        print(f"⚠️ ML model loading failed: {e}")
        print("⚠️ App will run without predictions")

    from routes import register_routes
    register_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)