from flask import Flask
import os
import logging
from config import config
from ml_utils import MLModelManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_diagnostics(app):
    """Run diagnostic checks"""
    print("\n🔍 RUNNING DIAGNOSTICS...")
    
    # Check file existence
    files_to_check = ['config.py', 'ml_utils.py', 'routes.py']
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} MISSING")
    
    # Check ML manager
    print(f"📊 ML Manager initialized: {hasattr(app, 'ml_manager')}")
    if hasattr(app, 'ml_manager'):
        print(f"📊 ML Models loaded: {app.ml_manager.is_loaded if hasattr(app.ml_manager, 'is_loaded') else 'Unknown'}")
    
    print("🔍 DIAGNOSTICS COMPLETE\n")

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

    # Run diagnostics
    run_diagnostics(app)

    # Register routes
    try:
        from routes import register_routes
        register_routes(app)
        print("✅ Routes registered successfully")
    except ImportError as e:
        print(f"❌ Failed to import routes: {e}")
    except Exception as e:
        print(f"❌ Failed to register routes: {e}")

    return app

if __name__ == '__main__':
    app = create_app()
    if app is not None:
        print("🚀 Starting Flask application...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to create Flask application")