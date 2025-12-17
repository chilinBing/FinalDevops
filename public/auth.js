// Authentication JavaScript

const API_BASE = '/api';

// Check if user is already logged in
function checkAuth() {
    const token = localStorage.getItem('token');
    if (token && window.location.pathname.includes('index.html')) {
        // Already logged in, stay on main page
        return true;
    } else if (token && (window.location.pathname.includes('login.html') || window.location.pathname.includes('register.html'))) {
        // Already logged in, redirect to main page
        window.location.href = 'index.html';
        return true;
    } else if (!token && window.location.pathname.includes('index.html')) {
        // Not logged in, redirect to login
        window.location.href = 'login.html';
        return false;
    }
    return !!token;
}

// Show message
function showMessage(message, type = 'error') {
    const messageDiv = document.getElementById('message');
    if (messageDiv) {
        messageDiv.textContent = message;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';
        
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }
}

// Login Form Handler
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        try {
            const response = await fetch(`${API_BASE}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Save token and user info
                localStorage.setItem('token', data.token);
                localStorage.setItem('user', JSON.stringify(data.user));
                
                showMessage('Login successful! Redirecting...', 'success');
                
                // Redirect to main page
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1000);
            } else {
                showMessage(data.error || 'Login failed');
            }
        } catch (error) {
            showMessage('Network error. Please try again.');
            console.error('Login error:', error);
        }
    });
}

// Register Form Handler
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        // Validate passwords match
        if (password !== confirmPassword) {
            showMessage('Passwords do not match');
            return;
        }
        
        try {
            const response = await fetch(`${API_BASE}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Save token and user info
                localStorage.setItem('token', data.token);
                localStorage.setItem('user', JSON.stringify(data.user));
                
                showMessage('Registration successful! Redirecting...', 'success');
                
                // Redirect to main page
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1000);
            } else {
                showMessage(data.error || 'Registration failed');
            }
        } catch (error) {
            showMessage('Network error. Please try again.');
            console.error('Registration error:', error);
        }
    });
}

// Check authentication on page load
checkAuth();
