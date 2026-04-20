"""
The Enhancer - Photo & Video Enhancement Service
Main entrypoint for Vercel deployment
"""

from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)

# Route for main sales page
@app.route('/')
def home():
    """Main sales page"""
    return send_from_directory('.', 'salespage-v1.html')

# Route for variation 1
@app.route('/v1')
def v1():
    """Sales page variation 1"""
    return send_from_directory('.', 'salespage-v1.html')

# Route for variation 2
@app.route('/v2')
def v2():
    """Sales page variation 2"""
    return send_from_directory('.', 'salespage-v2.html')

# Route for variation 3
@app.route('/v3')
def v3():
    """Sales page variation 3"""
    return send_from_directory('.', 'salespage-v3.html')

# API status endpoint
@app.route('/api/status')
def status():
    """API status endpoint"""
    return {
        "status": "operational",
        "service": "The Enhancer",
        "version": "1.0.0"
    }

if __name__ == '__main__':
    app.run(debug=True)
