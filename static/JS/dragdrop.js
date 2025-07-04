document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const submitBtn = document.getElementById('submit-btn');
    const removeFileBtn = document.getElementById('remove-file');

    // Supported file types
    const supportedTypes = ['.csv', '.xlsx', '.json', '.txt'];
    const maxFileSize = 16 * 1024 * 1024; // 16MB

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop area when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);

    // Handle click to select file
    dropZone.addEventListener('click', () => fileInput.click());

    // Handle file input change
    fileInput.addEventListener('change', handleFileSelect);

    // Handle remove file button
    if (removeFileBtn) {
        removeFileBtn.addEventListener('click', removeFile);
    }

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight(e) {
        dropZone.classList.add('drag-over');
    }

    function unhighlight(e) {
        dropZone.classList.remove('drag-over');
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    function handleFileSelect(e) {
        const files = e.target.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            
            // Validate file
            if (validateFile(file)) {
                displayFileInfo(file);
            }
        }
    }

    function validateFile(file) {
        // Check file size
        if (file.size > maxFileSize) {
            showAlert('File too large. Maximum size is 16MB.', 'error');
            return false;
        }

        // Check file type
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        if (!supportedTypes.includes(fileExtension)) {
            showAlert('Unsupported file type. Please upload CSV, Excel, JSON, or TXT files.', 'error');
            return false;
        }

        return true;
    }

    function displayFileInfo(file) {
        // Display filename
        fileName.textContent = file.name;
        
        // Display file size
        const size = formatFileSize(file.size);
        fileSize.textContent = `Size: ${size}`;
        
        // Show file info with animation
        fileInfo.classList.remove('d-none');
        
        // Hide drop zone
        dropZone.style.display = 'none';
        
        // Enable submit button and change style
        submitBtn.disabled = false;
        submitBtn.classList.remove('btn-secondary');
        submitBtn.classList.add('btn-success');
        
        console.log('File selected:', file.name, size);
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    function removeFile() {
        // Clear file input
        fileInput.value = '';
        
        // Hide file info and show drop zone
        fileInfo.classList.add('d-none');
        dropZone.style.display = 'block';
        
        // Disable submit button and reset style
        submitBtn.disabled = true;
        submitBtn.classList.remove('btn-success');
        submitBtn.classList.add('btn-secondary');
        
        // Clear file info
        fileName.textContent = '';
        fileSize.textContent = '';
        
        console.log('File removed');
    }

    function showAlert(message, type = 'info') {
        // Create alert element
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            <i class="bi bi-${type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert alert before the form
        const form = document.getElementById('upload-form');
        form.parentNode.insertBefore(alertDiv, form);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    // Initialize: Check if file input already has a file (for page refresh)
    if (fileInput.files && fileInput.files.length > 0) {
        handleFiles(fileInput.files);
    }
});