# filepath: d:\Categorizer U.I\routes.py
from flask import render_template, request, send_file, flash, redirect, url_for, jsonify
import pandas as pd
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import tempfile

def register_routes(app):
    
    # Define allowed extensions with fallback
    ALLOWED_EXTENSIONS = getattr(app.config, 'ALLOWED_EXTENSIONS', {'csv', 'xlsx', 'json', 'txt'})
    
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @app.route('/')
    def index():
        """Main menu page - Landing page"""
        return render_template('menu.html')
    
    @app.route('/data-categorizer')
    def data_categorizer():
        """Data categorizer page"""
        return render_template('data_categorizer.html')
    
    @app.route('/name-assign')
    def name_assign():
        """Name assignment page (placeholder)"""
        return "<h1>Name Assignment</h1><p>Coming soon!</p><a href='/'>Back to Menu</a>"
    
    @app.route('/upload', methods=['POST'])
    def upload():
        try:
            # Check if file was uploaded
            if 'datafile' not in request.files:
                flash('No file selected', 'error')
                return redirect('/data-categorizer')
            
            file = request.files['datafile']
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect('/data-categorizer')
            
            # Validate file type
            if not allowed_file(file.filename):
                flash('Invalid file type. Please upload CSV, Excel, JSON, or TXT files.', 'error')
                return redirect('/data-categorizer')
            
            # Get form data
            supplier_col = request.form.get('variable1', '').strip()
            description_col = request.form.get('variable2', '').strip()
            category_col = request.form.get('variable3', '').strip()
            output_format = request.form.get('output_format', 'excel')
            
            # Validate required fields
            if not description_col:
                flash('Description column name is required', 'error')
                return redirect('/data-categorizer')
            
            print(f"📊 Processing file: {file.filename}")
            print(f"📋 Description column: {description_col}")
            print(f"📤 Output format: {output_format}")
            
            # Read the uploaded file
            df = read_uploaded_file(file)
            print(f"📊 File loaded: {len(df)} rows, {len(df.columns)} columns")
            print(f"📋 Available columns: {list(df.columns)}")
            
            # Validate that the description column exists
            if description_col not in df.columns:
                available_cols = ', '.join(df.columns)
                flash(f'Column "{description_col}" not found. Available columns: {available_cols}', 'error')
                return redirect('/data-categorizer')
            
            # Process with ML model if available
            if hasattr(app, 'ml_manager') and app.ml_manager and app.ml_manager.is_loaded:
                try:
                    print("🤖 Running ML predictions...")
                    df = app.ml_manager.predict_categories(df, description_col)
                    flash('Data processed successfully with ML predictions!', 'success')
                except Exception as e:
                    print(f"❌ ML processing failed: {e}")
                    flash(f'ML processing failed: {str(e)}', 'warning')
            else:
                print("⚠️ ML models not available")
                if hasattr(app, 'ml_manager'):
                    print(f"ML Manager exists: {app.ml_manager is not None}")
                    if app.ml_manager:
                        print(f"ML Models loaded: {app.ml_manager.is_loaded}")
                else:
                    print("ML Manager not found in app")
                flash('ML models not available - returning original data', 'warning')
            
            # Generate output file
            output_file = generate_output_file(df, output_format)
            
            return send_file(
                output_file,
                as_attachment=True,
                download_name=f'categorized_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.{get_file_extension(output_format)}'
            )
            
        except Exception as e:
            print(f"❌ Error processing data: {e}")
            flash(f'Error processing data: {str(e)}', 'error')
            return redirect('/data-categorizer')

def read_uploaded_file(file):
    """Read uploaded file based on its extension"""
    filename = file.filename.lower()
    
    try:
        if filename.endswith('.csv'):
            return pd.read_csv(file)
        elif filename.endswith('.xlsx'):
            try:
                return pd.read_excel(file, engine='openpyxl')
            except ImportError:
                raise Exception("openpyxl is required for Excel files. Install with: pip install openpyxl")
        elif filename.endswith('.json'):
            return pd.read_json(file)
        elif filename.endswith('.txt'):
            return pd.read_csv(file, sep='\t')
        else:
            raise Exception(f"Unsupported file format: {filename}")
    except Exception as e:
        raise Exception(f"Failed to read file: {str(e)}")

def generate_output_file(df, output_format):
    """Generate output file in the requested format"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{get_file_extension(output_format)}') as tmp:
        try:
            if output_format == 'excel':
                df.to_excel(tmp.name, index=False, engine='openpyxl')
            elif output_format == 'csv':
                df.to_csv(tmp.name, index=False)
            elif output_format == 'json':
                df.to_json(tmp.name, orient='records', indent=2)
            
            return tmp.name
        except Exception as e:
            if output_format == 'excel':
                raise Exception("Excel export failed. Install openpyxl: pip install openpyxl")
            raise Exception(f"Failed to generate {output_format} file: {str(e)}")

def get_file_extension(output_format):
    """Get file extension for output format"""
    extensions = {
        'excel': 'xlsx',
        'csv': 'csv',
        'json': 'json'
    }
    return extensions.get(output_format, 'xlsx')