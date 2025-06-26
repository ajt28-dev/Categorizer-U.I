// Data Categorizer - Single File Drag & Drop with PASIA Styling
document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const submitBtn = document.getElementById('submit-btn');
    const confidenceSlider = document.getElementById('variable2');
    const confidenceValue = document.getElementById('confidence-value');
    
    // Update confidence value display
    confidenceSlider.addEventListener('input', function() {
        confidenceValue.textContent = this.value + '%';
    });
    
    // PASIA color scheme
    const pasiaColors = {
        greenPrimary: '#2d6d2a',
        greenLight: '#56d35a',
        blueDark: '#304757',
        blueMedium: '#466073',
        blueLight: '#16697A'
    };
    
    // File validation
    function isValidFile(file) {
        const validTypes = [
            'text/csv',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/json',
            'text/plain'
        ];
        const maxSize = 50 * 1024 * 1024; // 50MB
        
        if (!validTypes.includes(file.type) && !file.name.match(/\.(csv|xlsx|json|txt)$/i)) {
            alert('Please upload a valid file format (CSV, Excel, JSON, or TXT)');
            return false;
        }
        
        if (file.size > maxSize) {
            alert('File size must be less than 50MB');
            return false;
        }
        
        return true;
    }
    
    // Format file size
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // Handle file selection
    function handleFile(file) {
        if (isValidFile(file)) {
            fileName.textContent = file.name;
            fileSize.textContent = formatFileSize(file.size);
            fileInfo.style.display = 'block';
            
            // Update drop zone appearance
            dropZone.style.border = `3px solid ${pasiaColors.greenPrimary}`;
            dropZone.style.background = `linear-gradient(135deg, rgba(45, 109, 42, 0.1) 0%, rgba(86, 211, 90, 0.2) 100%)`;
            
            // Enable submit button
            checkFormValidity();
        }
    }
    
    // Check if form is valid
    function checkFormValidity() {
        const hasFile = fileInput.files.length > 0;
        const hasVariable1 = document.getElementById('variable1').value !== '';
        
        if (hasFile && hasVariable1) {
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
            submitBtn.style.cursor = 'pointer';
        } else {
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.6';
            submitBtn.style.cursor = 'not-allowed';
        }
    }
    
    // Click to upload
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });
    
    // Drag and drop events
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.border = `3px dashed ${pasiaColors.blueLight}`;
        dropZone.style.background = `linear-gradient(135deg, rgba(22, 105, 122, 0.1) 0%, rgba(86, 211, 90, 0.1) 100%)`;
        dropZone.style.transform = 'scale(1.02)';
    });
    
    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.style.border = `3px dashed ${pasiaColors.greenLight}`;
        dropZone.style.background = `linear-gradient(135deg, rgba(86, 211, 90, 0.1) 0%, rgba(48, 71, 87, 0.1) 100%)`;
        dropZone.style.transform = 'scale(1)';
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.border = `3px dashed ${pasiaColors.greenLight}`;
        dropZone.style.background = `linear-gradient(135deg, rgba(86, 211, 90, 0.1) 0%, rgba(48, 71, 87, 0.1) 100%)`;
        dropZone.style.transform = 'scale(1)';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFile(files[0]);
        }
    });
    
    // Monitor form changes
    document.getElementById('variable1').addEventListener('change', checkFormValidity);
    
    // Form submission with loading state
    document.getElementById('upload-form').addEventListener('submit', function(e) {
        if (!submitBtn.disabled) {
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            submitBtn.disabled = true;
        }
    });
    
    // Add hover effects to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            if (!this.disabled) {
                this.style.transform = 'translateY(-2px)';
                this.style.transition = 'all 0.3s ease';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    console.log('Data Categorizer loaded successfully with PASIA styling');
});
