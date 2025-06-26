// Main JavaScript for PASIA Data Master
document.addEventListener('DOMContentLoaded', function() {
    console.log('PASIA Data Master loaded successfully');
    
    // Add hover effects to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.transition = 'all 0.3s ease';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Add click effects
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Loading animation for navigation
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Add loading spinner
            const originalText = this.innerHTML;
            this.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Loading...';
            this.classList.add('disabled');
            
            // Simulate loading (remove this in production)
            setTimeout(() => {
                window.location.href = this.href;
            }, 500);
            
            e.preventDefault();
        });
    });
});

// Add some custom animations
const style = document.createElement('style');
style.textContent = `
    /* PASIA Color Scheme */
    :root {
        --pasia-green-primary: #2d6d2a;
        --pasia-green-light: #56d35a;
        --pasia-blue-dark: #304757;
        --pasia-blue-medium: #466073;
        --pasia-blue-light: #16697A;
    }
    
    /* Custom PASIA Buttons */
    .pasia-btn-primary {
        background: linear-gradient(135deg, var(--pasia-green-primary) 0%, var(--pasia-green-light) 100%);
        border: none;
        color: white;
        font-weight: 600;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(45, 109, 42, 0.3);
        transition: all 0.3s ease;
    }
    
    .pasia-btn-primary:hover {
        background: linear-gradient(135deg, var(--pasia-green-light) 0%, var(--pasia-green-primary) 100%);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(45, 109, 42, 0.4);
        color: white;
    }
    
    .pasia-btn-secondary {
        background: linear-gradient(135deg, var(--pasia-blue-dark) 0%, var(--pasia-blue-light) 100%);
        border: none;
        color: white;
        font-weight: 600;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(48, 71, 87, 0.3);
        transition: all 0.3s ease;
    }
    
    .pasia-btn-secondary:hover {
        background: linear-gradient(135deg, var(--pasia-blue-light) 0%, var(--pasia-blue-dark) 100%);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(48, 71, 87, 0.4);
        color: white;
    }
    
    /* Card styling with PASIA colors */
    .card {
        border: 2px solid var(--pasia-blue-dark);
        border-radius: 15px;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .card {
        animation: fadeInUp 0.8s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Background gradient */
    body {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
`;
document.head.appendChild(style);
