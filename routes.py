from flask import render_template, request, flash, redirect, url_for, send_file
from ml_utils import ml_manager
import pandas as pd
import io
from datetime import date

def register_routes(app):
    
    @app.route('/')
    def dashboard():
        return render_template('menu.html')
    
    @app.route('/data_categorizer', methods=['GET', 'POST'])
    def data_categorizer():
        if request.method == 'POST':
            return upload()
        return render_template('data_categorizer.html')
    
    @app.route('/upload', methods=['POST'])
    def upload():
        try:
            # 1. Validate file upload
            if 'datafile' not in request.files:
                flash('No file selected', 'error')
                return redirect(url_for('data_categorizer'))
            
            file = request.files['datafile']
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(url_for('data_categorizer'))
            
            # 2. Get form data with NEW structure
            form_data = {
                'supplier_column': request.form.get('variable1', '').strip(),
                'description_column': request.form.get('variable2', '').strip(),
                'categorization_column': request.form.get('variable3', '').strip(),  # NEW!
                'output_format': request.form.get('output_format', 'excel')          # RENAMED!
            }
            
            # 3. Validate required fields
            if not form_data['description_column']:
                flash('Description column name is required!', 'error')
                return redirect(url_for('data_categorizer'))
            
            # 4. Read uploaded file
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                flash('Unsupported file format. Please upload CSV or Excel files.', 'error')
                return redirect(url_for('data_categorizer'))
            
            # 5. Validate column names exist in the file
            if form_data['description_column'] not in df.columns:
                flash(f'Column "{form_data["description_column"]}" not found in file!', 'error')
                return redirect(url_for('data_categorizer'))
            
            if form_data['supplier_column'] and form_data['supplier_column'] not in df.columns:
                flash(f'Supplier column "{form_data["supplier_column"]}" not found in file!', 'warning')
            
            if form_data['categorization_column'] and form_data['categorization_column'] not in df.columns:
                flash(f'Categorization column "{form_data["categorization_column"]}" not found in file!', 'warning')
            
            # 6. Apply ML predictions
            df = ml_manager.predict_categories(df, form_data['description_column'])
            
            # 7. Generate output based on selected format
            output_filename = f"categorized_data_{date.today().strftime('%d-%m-%Y')}"
            
            if form_data['output_format'] == 'excel':
                output = io.BytesIO()
                df.to_excel(output, index=False)
                output.seek(0)
                filename = f"{output_filename}.xlsx"
                mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                
            elif form_data['output_format'] == 'csv':
                output = io.StringIO()
                df.to_csv(output, index=False)
                output = io.BytesIO(output.getvalue().encode('utf-8'))
                output.seek(0)
                filename = f"{output_filename}.csv"
                mimetype = 'text/csv'
                
            elif form_data['output_format'] == 'json':
                output = io.BytesIO()
                json_data = df.to_json(orient='records', indent=2)
                output.write(json_data.encode('utf-8'))
                output.seek(0)
                filename = f"{output_filename}.json"
                mimetype = 'application/json'
            
            else:
                # Default to Excel
                output = io.BytesIO()
                df.to_excel(output, index=False)
                output.seek(0)
                filename = f"{output_filename}.xlsx"
                mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            
            flash('✅ Data categorized successfully!', 'success')
            return send_file(output, mimetype=mimetype, as_attachment=True, download_name=filename)
            
        except Exception as e:
            flash(f'Error processing data: {str(e)}', 'error')
            return redirect(url_for('data_categorizer'))