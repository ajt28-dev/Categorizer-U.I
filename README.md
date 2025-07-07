# 📊 PASIA Data Categorizer

A Flask-based web application for automated data categorization using machine learning. This tool processes uploaded data files and automatically categorizes items based on their descriptions using trained ML models.

## 🌟 Features

- **📁 Multi-format File Support**: Upload CSV, Excel (.xlsx), JSON, and TXT files
- **🤖 ML-Powered Categorization**: Automatic item classification using trained models
- **📤 Multiple Output Formats**: Export results as Excel, CSV, or JSON
- **🎯 Column Mapping**: Flexible column configuration for different data structures
- **🖱️ Drag & Drop Interface**: User-friendly file upload with visual feedback
- **⚡ Real-time Processing**: Live progress indicators and file validation
- **🔒 Secure Processing**: Local data processing with no external data transmission

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **ML Framework**: scikit-learn, joblib
- **Data Processing**: pandas, numpy
- **File Handling**: openpyxl, xlsxwriter

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "Categorizer U.I"
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up ML Models
Ensure your trained models are placed in the `models/` directory:
```
models/
├── ayala_categorizer.joblib      # Trained ML model
└── ayala_label_encoder.joblib    # Label encoder
```

### 5. Run the Application
```bash
python app.py
```

Visit `http://localhost:5000` to access the application.

## 📁 Project Structure

```
Categorizer U.I/
│
├── app.py                     # Main Flask application
├── config.py                  # Configuration settings
├── ml_utils.py               # ML model management
├── routes.py                 # Flask routes and handlers
├── requirements.txt          # Python dependencies
│
├── templates/                # HTML templates
│   ├── menu.html            # Main menu page
│   └── data_categorizer.html # Data categorizer interface
│
├── static/                   # Static assets
│   ├── css/
│   │   ├── style.css        # Menu page styles
│   │   └── data_categorizer.css # Categorizer page styles
│   └── js/
│       └── dragdrop.js      # File upload functionality
│
├── models/                   # ML model files
│   ├── ayala_categorizer.joblib
│   └── ayala_label_encoder.joblib
│
├── uploads/                  # Temporary file storage
└── README.md                # Project documentation
```

## 💻 Usage

### 1. **Access Main Menu**
   - Navigate to `http://localhost:5000`
   - Choose "Data Categorizer" from the menu

### 2. **Upload Data File**
   - Drag and drop your file or click to browse
   - Supported formats: CSV, Excel (.xlsx), JSON, TXT
   - Maximum file size: 16MB

### 3. **Configure Columns**
   - **Description Column** (Required): Column containing item descriptions
   - **Supplier Column** (Optional): Column with supplier information
   - **Categorization Column** (Optional): Existing category column

### 4. **Select Output Format**
   - Choose from Excel (.xlsx), CSV (.csv), or JSON (.json)

### 5. **Process Data**
   - Click "Process Data" to run ML categorization
   - Download the processed file automatically

## 🤖 Machine Learning Integration

The application uses trained ML models to automatically categorize items:

- **Model Type**: Text classification using scikit-learn
- **Input**: Item descriptions (text data)
- **Output**: Hierarchical categories (S/NS, Major Category, Minor Category)
- **Processing**: TF-IDF vectorization + trained classifier

### Model Requirements
- **Main Model**: `ayala_categorizer.joblib`
- **Label Encoder**: `ayala_label_encoder.joblib`
- **Format**: joblib serialized scikit-learn models

## ⚙️ Configuration

### Environment Variables
```bash
SECRET_KEY=your-secret-key-here    # Flask secret key
```

### Application Settings (config.py)
```python
UPLOAD_FOLDER = 'uploads'          # File upload directory
MAX_CONTENT_LENGTH = 16MB          # Maximum file size
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'json', 'txt'}
```

## 🔧 Development

### Running in Development Mode
```bash
export FLASK_ENV=development  # Linux/macOS
set FLASK_ENV=development     # Windows
python app.py
```

### Testing ML Models
```bash
python -c "from ml_utils import test_model_loading; test_model_loading()"
```

### File Structure for Development
```
├── templates/           # Jinja2 templates
├── static/             # CSS, JS, images
├── models/             # ML model files
└── uploads/            # Temporary uploads (auto-created)
```

## 🐛 Troubleshooting

### Common Issues

1. **"ML models not loaded"**
   ```bash
   # Check if model files exist
   ls models/
   # Should show: ayala_categorizer.joblib, ayala_label_encoder.joblib
   ```

2. **"openpyxl not found"**
   ```bash
   pip install openpyxl
   ```

3. **"Column not found in file"**
   - Verify column names match exactly (case-sensitive)
   - Check for extra spaces or special characters

4. **File upload fails**
   - Ensure file is under 16MB
   - Check file format is supported
   - Verify file is not corrupted

### Debug Mode
Enable debug mode for detailed error messages:
```python
app.run(debug=True)
```

## 📊 Supported Data Formats

### Input Formats
- **CSV**: Comma-separated values
- **Excel**: .xlsx files (requires openpyxl)
- **JSON**: JavaScript Object Notation
- **TXT**: Tab-separated text files

### Output Formats
- **Excel**: .xlsx with formatting
- **CSV**: Standard comma-separated
- **JSON**: Structured data format

## 🔐 Security Features

- File type validation
- File size limits
- Secure filename handling
- Local processing (no data leaves your server)
- CSRF protection via Flask

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **PASIA Team** - Initial development

## 🙏 Acknowledgments

- Flask community for the excellent web framework
- scikit-learn team for ML capabilities
- Bootstrap team for responsive UI components

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team

## 🔄 Version History

- **v1.0.0** - Initial release with basic categorization
- **v1.1.0** - Added drag-and-drop file upload
- **v1.2.0** - Enhanced ML model integration
- **v1.3.0** - Multi-format output support

---

**📊 PASIA Data Categorizer** - Streamlining data classification with machine learning