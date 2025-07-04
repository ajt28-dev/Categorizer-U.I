from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, send_file
import os
import pandas as pd
from tqdm import tqdm
from datetime import date
import pickle
import io

# Create Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Needed for flash messages

# --- ⚙️ ML MODEL CONFIGURATIONS ---
MODEL_PATH = "models/ayala_categorizer.joblib"  # Adjust path as needed
LABEL_ENCODER_PATH = "models/ayala_label_encoder.joblib"  # Adjust path as needed

# Column names
COL_DESCRIPTION = "Description"
COL_SNS = "S/NS"
COL_MAJOR = "Major Category"
COL_MINOR = "Minor Category"
COL_DATE = "Date"

# Load ML model and label encoder at startup
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(LABEL_ENCODER_PATH, 'rb') as f:
        label_encoder = pickle.load(f)
    print("✅ ML models loaded successfully")
except Exception as e:
    print(f"❌ Error loading ML models: {e}")
    model = None
    label_encoder = None

def predict_categories(df, description_column):
    """Apply ML prediction to the dataframe"""
    if model is None or label_encoder is None:
        raise Exception("ML models not loaded")
    
    # Prepare description column
    df[description_column] = df[description_column].astype(str).str.lower().str.strip()
    
    # Predict categories
    print("🔍 Predicting categories...")
    preds = list(tqdm(model.predict(df[description_column]), total=len(df), desc="⏳ Predicting"))
    
    # Decode predicted labels
    print("🔓 Decoding labels...")
    decoded_labels = list(tqdm(label_encoder.inverse_transform(preds), total=len(preds), desc="🔄 Decoding"))
    
    # Split decoded labels into components
    pred_df = pd.DataFrame(decoded_labels, columns=['Combined'])
    pred_df[[COL_SNS, COL_MAJOR, COL_MINOR]] = pred_df['Combined'].str.split(" \| ", expand=True)
    pred_df.drop(columns=['Combined'], inplace=True)
    pred_df[COL_DATE] = date.today().strftime("%d-%m-%Y")
    
    # Add prediction columns if they don't exist
    for col in [COL_SNS, COL_MAJOR, COL_MINOR, COL_DATE]:
        if col not in df.columns:
            df[col] = ""
    
    # Fill only if current values are missing or blank
    print("✏️ Updating missing prediction fields...")
    for col in [COL_SNS, COL_MAJOR, COL_MINOR, COL_DATE]:
        mask = df[col].isna() | (df[col].astype(str).str.strip() == "")
        df.loc[mask, col] = pred_df.loc[mask, col]
    
    return df

@app.route('/')
def dashboard():
    return render_template('menu.html')

@app.route('/data_categorizer', methods=['GET', 'POST'])
def data_categorizer():
    if request.method == 'POST':
        # Handle POST request (form submission)
        return upload()
    else:
        # Handle GET request (display form)
        return render_template('data_categorizer.html')

# Add the missing upload route
@app.route('/upload', methods=['POST'])
def upload():
   
   if 'datafile' not in request.files:
        flash('No file part in the request')
        return redirect(url_for('data_categorizer'))
   
   file = request.files['datafile']

   if file.filename == '':
        flash('No selected file')
        return redirect(url_for('data_categorizer'))
   
   allowed_extensions = {'csv', 'xlsx'}
   file_extension = file.filename.rsplit('.',1 )[1].lower() if '.'in file.filename else''

   if file_extension not in allowed_extensions:
       flash('Invalid file type. Please upload a CSV or Excel file.')
       return redirect(url_for('data_categorizer'))
   
   #get form data

   supplier_column = request.form.get('variable1').strip()
   description_column = request.form.get('variable2','').strip()
   output_format = request.form.get('variable3')
   if not description_column:
       flash('Description column is required!', 'error')
       return redirect(url_for('data_categorizer'))
   
   try:
       if file.filename.endswith('.csv'):
           df = pd.read_csv(file)
       elif file.filename.endswith('.xlsx'):
           df = pd.read_excel(file)
       elif file.filename.endswith('.xls'):
           df = pd.read_excel(file, engine='xlrd')

   except Exception as e:
       flash(f'Error reading file: {str(e)}', 'error')
       return redirect(url_for('data_categorizer'))

   use_supplier = False
   if supplier_column:
       if supplier_column in df.columns:
           use_supplier = True
           flash(f'Processing with supplier column: "{supplier_column}"', 'info')
       else:
           flash('No supplier column provided, processing without it.', 'warning')
   else:
       flash('No supplier column specified', 'info')
   
   if description_column not in df.columns:
       flash(f'Description column "{description_column}" not found in file!', 'error')
       return redirect(url_for('data_categorizer'))
   try:
       if use_supplier:
           # Process with supplier column
           df[supplier_column] = df[supplier_column].astype(str)
           df[description_column] = df[description_column].astype(str)
           
           # Apply ML prediction
           df = predict_categories(df, description_column)
           
       else:
           df[description_column] = df[description_column].astype(str)
           
           # Apply ML prediction
           df = predict_categories(df, description_column)
       
       # Generate output filename
       output_filename = f"categorized_data_{date.today().strftime('%d-%m-%Y')}.xlsx"
       
       # Save to memory buffer
       output = io.BytesIO()
       df.to_excel(output, index=False)
       output.seek(0)
       
       flash('✅ Data categorized successfully!', 'success')
       
       # Return file for download
       return send_file(
           output,
           mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
           as_attachment=True,
           download_name=output_filename
       )
       
   except Exception as e:
       flash(f'Error processing data: {str(e)}', 'error')
       return redirect(url_for('data_categorizer'))


# Run the app
if __name__ == '__main__':
    app.run(debug=True)