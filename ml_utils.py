import pickle
import pandas as pd
from tqdm import tqdm
from datetime import date
import logging

logger = logging.getLogger(__name__)

# --- ⚙️ ML MODEL CONFIGURATIONS ---
MODEL_PATH = "models/ayala_categorizer.joblib"
LABEL_ENCODER_PATH = "models/ayala_label_encoder.joblib"

# Column names
COL_DESCRIPTION = "Description"
COL_SNS = "S/NS"
COL_MAJOR = "Major Category"
COL_MINOR = "Minor Category"
COL_DATE = "Date"

class MLModelManager:
    """Manages ML model loading and predictions"""
    
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.is_loaded = False
    
    def load_models(self, model_path=None, encoder_path=None):
        """Load ML models with error handling"""
        # Use default paths if not provided
        if model_path is None:
            model_path = MODEL_PATH
        if encoder_path is None:
            encoder_path = LABEL_ENCODER_PATH
        
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            with open(encoder_path, 'rb') as f:
                self.label_encoder = pickle.load(f)
            
            self.is_loaded = True
            print("✅ ML models loaded successfully")
            logger.info("ML models loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error loading ML models: {e}")
            logger.error(f"Error loading ML models: {e}")
            self.model = None
            self.label_encoder = None
            self.is_loaded = False
            return False
    
    def predict_categories(self, df, description_column):
        """Apply ML prediction to the dataframe"""
        if not self.is_loaded or self.model is None or self.label_encoder is None:
            raise Exception("ML models not loaded")
        
        # Prepare description column
        df[description_column] = df[description_column].astype(str).str.lower().str.strip()
        
        # Predict categories
        print("🔍 Predicting categories...")
        preds = list(tqdm(self.model.predict(df[description_column]), total=len(df), desc="⏳ Predicting"))
        
        # Decode predicted labels
        print("🔓 Decoding labels...")
        decoded_labels = list(tqdm(self.label_encoder.inverse_transform(preds), total=len(preds), desc="🔄 Decoding"))
        
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

# Legacy function for backward compatibility (if needed)
def predict_categories(df, description_column):
    """Legacy function - creates a temporary MLModelManager instance"""
    manager = MLModelManager()
    if manager.load_models():
        return manager.predict_categories(df, description_column)
    else:
        raise Exception("ML models could not be loaded")
    

# ... (keep all your existing code above)

# Add this at the end of the file:
ml_manager = MLModelManager()