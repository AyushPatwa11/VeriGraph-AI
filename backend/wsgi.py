"""
WSGI entry point for production deployment
Can be used with Gunicorn or other WSGI servers
"""

import os
from app import app, cache_manager, metrics_collector

# Configure for production
if __name__ == "__main__":
    # Set environment variables for production
    os.environ.setdefault('FLASK_ENV', 'production')
    
    # Initialize the app with production settings
    app.config.from_object('config.ProductionConfig')
    
    # Application starts with cache_manager and metrics_collector pre-initialized
    print("VeriGraph backend starting in production mode...")
else:
    # For WSGI servers like Gunicorn
    application = app
