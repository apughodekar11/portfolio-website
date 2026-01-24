// ============================================
// CONTACT FORM HANDLER - Calls AWS API Gateway
// ============================================

const ContactForm = {
    // API endpoint (will be your CloudFront domain + /api/contact)
    // This is set after deployment - update this!
    API_ENDPOINT: '/api/contact',
    
    // Form elements
    form: null,
    submitBtn: null,
    
    // Initialize
    init() {
        this.form = document.getElementById('contact-form');
        if (!this.form) return;
        
        this.submitBtn = this.form.querySelector('.form-submit');
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    },
    
    // Validate form
    validate() {
        const name = this.form.querySelector('#name').value.trim();
        const email = this.form.querySelector('#email').value.trim();
        const message = this.form.querySelector('#message').value.trim();
        
        const errors = [];
        
        if (name.length < 2) {
            errors.push('Name must be at least 2 characters');
        }
        
        if (!this.isValidEmail(email)) {
            errors.push('Please enter a valid email address');
        }
        
        if (message.length < 10) {
            errors.push('Message must be at least 10 characters');
        }
        
        return errors;
    },
    
    // Email validation
    isValidEmail(email) {
        const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return pattern.test(email);
    },
    
    // Show loading state
    setLoading(loading) {
        if (loading) {
            this.submitBtn.disabled = true;
            this.submitBtn.innerHTML = `
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
                    <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32"></circle>
                </svg>
                Sending...
            `;
        } else {
            this.submitBtn.disabled = false;
            this.submitBtn.innerHTML = `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="22" y1="2" x2="11" y2="13"></line>
                    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                </svg>
                Send Message
            `;
        }
    },
    
    // Show success state
    setSuccess() {
        this.submitBtn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            Message Sent!
        `;
        this.submitBtn.style.background = 'var(--accent-green)';
        
        // Reset after 3 seconds
        setTimeout(() => {
            this.setLoading(false);
            this.submitBtn.style.background = '';
            this.form.reset();
        }, 3000);
    },
    
    // Show error state
    setError(message) {
        this.submitBtn.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="15" y1="9" x2="9" y2="15"></line>
                <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
            Failed - Try Again
        `;
        this.submitBtn.style.background = 'var(--accent-red)';
        
        // Show error message
        this.showNotification(message, 'error');
        
        // Reset after 3 seconds
        setTimeout(() => {
            this.setLoading(false);
            this.submitBtn.style.background = '';
        }, 3000);
    },
    
    // Show notification
    showNotification(message, type = 'info') {
        // Remove existing notification
        const existing = document.querySelector('.form-notification');
        if (existing) existing.remove();
        
        const notification = document.createElement('div');
        notification.className = `form-notification ${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button onclick="this.parentElement.remove()">×</button>
        `;
        
        this.form.insertBefore(notification, this.form.firstChild);
        
        // Auto remove after 5 seconds
        setTimeout(() => notification.remove(), 5000);
    },
    
    // Handle form submission
    async handleSubmit(e) {
        e.preventDefault();
        
        // Validate
        const errors = this.validate();
        if (errors.length > 0) {
            this.showNotification(errors.join('. '), 'error');
            return;
        }
        
        // Get form data
        const formData = {
            name: this.form.querySelector('#name').value.trim(),
            email: this.form.querySelector('#email').value.trim(),
            subject: this.form.querySelector('#subject')?.value.trim() || '',
            message: this.form.querySelector('#message').value.trim()
        };
        
        // Set loading state
        this.setLoading(true);
        
        try {
            const response = await fetch(this.API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                this.setSuccess();
            } else {
                throw new Error(data.message || 'Failed to send message');
            }
            
        } catch (error) {
            console.error('Contact form error:', error);
            this.setError(error.message || 'Failed to send message. Please try again.');
        }
    }
};

// Add CSS for notifications and spinner
const style = document.createElement('style');
style.textContent = `
    .form-notification {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    
    .form-notification.error {
        background: rgba(248, 113, 113, 0.1);
        border: 1px solid rgba(248, 113, 113, 0.3);
        color: var(--accent-red);
    }
    
    .form-notification.success {
        background: rgba(52, 211, 153, 0.1);
        border: 1px solid rgba(52, 211, 153, 0.3);
        color: var(--accent-green);
    }
    
    .form-notification button {
        background: none;
        border: none;
        color: inherit;
        font-size: 1.25rem;
        cursor: pointer;
        padding: 0 0.5rem;
    }
    
    .spin {
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    ContactForm.init();
});
