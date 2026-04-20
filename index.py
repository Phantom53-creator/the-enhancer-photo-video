"""
The Enhancer - Photo & Video Enhancement Service
Permanent Flask app with proper static file routing
"""

from flask import Flask, send_from_directory, render_template_string, abort
import os

app = Flask(__name__)

# Helper function to safely serve HTML files
def serve_html(filename):
    """Serve HTML file from root directory"""
    try:
        if os.path.exists(filename):
            return send_from_directory('.', filename)
        else:
            abort(404)
    except Exception as e:
        return f"Error serving {filename}: {str(e)}", 500

# Main route - serves the primary sales page
@app.route('/')
def home():
    """Main landing page"""
    return serve_html('salespage-v1.html')

# Static HTML page routes
@app.route('/<page>')
def serve_page(page):
    """Serve specific HTML pages"""
    # List of valid pages
    valid_pages = ['v1', 'v2', 'v3', 'salespage-v1', 'salespage-v2', 'salespage-v3']
    
    if page in valid_pages:
        if page == 'v1':
            return serve_html('salespage-v1.html')
        elif page == 'v2':
            return serve_html('salespage-v2.html')
        elif page == 'v3':
            return serve_html('salespage-v3.html')
        else:
            return serve_html(f'{page}.html')
    
    # If not a valid page, return 404
    abort(404)

# API endpoints
@app.route('/api/status')
def status():
    """API status endpoint"""
    return {
        "status": "operational",
        "service": "The Enhancer",
        "version": "1.0.0",
        "pages_available": ["v1", "v2", "v3"]
    }

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Page Not Found - The Enhancer</title></head>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
        <h1>404 - Page Not Found</h1>
        <p>The page you're looking for doesn't exist.</p>
        <p><a href="/">Go to Home</a></p>
    </body>
    </html>
    """, 404

if __name__ == '__main__':
    app.run(debug=True)
