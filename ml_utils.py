import joblib
import pickle
import pandas as pd
from tqdm import tqdm
from datetime import date
import logging
import os

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
        print("🔧 MLModelManager initialized")
    
    def load_models(self, model_path=None, encoder_path=None):
        """Load ML models with comprehensive error handling"""
        # Use default paths if not provided
        if model_path is None:
            model_path = MODEL_PATH
        if encoder_path is None:
            encoder_path = LABEL_ENCODER_PATH
        
        print(f"🔍 Attempting to load models...")
        print(f"📂 Model path: {model_path}")
        print(f"📂 Encoder path: {encoder_path}")
        
        try:
            # Check if model directory exists
            models_dir = os.path.dirname(model_path)
            if not os.path.exists(models_dir):
                print(f"❌ Models directory not found: {models_dir}")
                print(f"💡 Create directory: mkdir {models_dir}")
                logger.error(f"Models directory not found: {models_dir}")
                return False
            
            # Check if model file exists
            if not os.path.exists(model_path):
                print(f"❌ Model file not found: {model_path}")
                print(f"💡 Available files in models/:")
                try:
                    files = os.listdir(models_dir)
                    for file in files:
                        print(f"   - {file}")
                except:
                    print("   (Cannot list directory contents)")
                logger.error(f"Model file not found: {model_path}")
                return False
                
            # Check if encoder file exists
            if not os.path.exists(encoder_path):
                print(f"❌ Encoder file not found: {encoder_path}")
                logger.error(f"Encoder file not found: {encoder_path}")
                return False
            
            # Load model
            print(f"📥 Loading model from: {model_path}")
            self.model = joblib.load(model_path)
            print(f"✅ Model loaded: {type(self.model)}")
            
            # Load encoder
            print(f"📥 Loading encoder from: {encoder_path}")
            self.label_encoder = joblib.load(encoder_path)
            print(f"✅ Encoder loaded: {type(self.label_encoder)}")
            
            self.is_loaded = True
            print("🎉 ML models loaded successfully!")
            logger.info("ML models loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error loading ML models: {e}")
            print(f"💡 Check if your model files are valid joblib files")
            logger.error(f"Error loading ML models: {e}")
            self.model = None
            self.label_encoder = None
            self.is_loaded = False
            return False
    
    def predict_categories(self, df, description_column):
        """Apply ML prediction to the dataframe"""
        if not self.is_loaded:
            raise Exception("ML models not loaded. Call load_models() first.")
        
        if self.model is None or self.label_encoder is None:
            raise Exception("ML models are None. Check model loading.")
        
        print(f"🔍 Starting prediction on {len(df)} rows...")
        print(f"📊 Using description column: {description_column}")
        
        # Validate description column exists
        if description_column not in df.columns:
            raise Exception(f"Description column '{description_column}' not found in dataframe")
        
        # Prepare description column
        df[description_column] = df[description_column].astype(str).str.lower().str.strip()
        
        # Predict categories
        print("🔍 Predicting categories...")
        try:
            preds = list(tqdm(self.model.predict(df[description_column]), total=len(df), desc="⏳ Predicting"))
            print(f"✅ Predictions completed: {len(preds)} predictions made")
        except Exception as e:
            raise Exception(f"Model prediction failed: {e}")
        
        # Decode predicted labels
        print("🔓 Decoding labels...")
        try:
            decoded_labels = list(tqdm(self.label_encoder.inverse_transform(preds), total=len(preds), desc="🔄 Decoding"))
            print(f"✅ Label decoding completed: {len(decoded_labels)} labels decoded")
        except Exception as e:
            raise Exception(f"Label decoding failed: {e}")
        
        # Split decoded labels into components
        print("📊 Processing predictions...")
        try:
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
            
            print("🎉 Prediction process completed successfully!")
            return df
            
        except Exception as e:
            raise Exception(f"Error processing predictions: {e}")

# Test function to check if models can be loaded
def test_model_loading():
    """Test function to check model loading"""
    print("🧪 Testing ML model loading...")
    manager = MLModelManager()
    success = manager.load_models()
    
    if success:
        print("✅ Model loading test PASSED")
        return True
    else:
        print("❌ Model loading test FAILED")
        return False

# Legacy function for backward compatibility
def predict_categories(df, description_column):
    """Legacy function - creates a temporary MLModelManager instance"""
    manager = MLModelManager()
    if manager.load_models():
        return manager.predict_categories(df, description_column)
    else:
        raise Exception("ML models could not be loaded")

# Create global instance
ml_manager = MLModelManager()

if __name__ == "__main__":
    # Run test when script is executed directly
    test_model_loading()