#!/usr/bin/env python3
"""
MFA Manager - TOTP Code Generator
A secure Flask application for managing MFA secrets and generating TOTP codes.
"""

import os
from app import app, db

def create_database():
    """Initialize the database with all tables"""
    with app.app_context():
        # Create all database tables
        db.create_all()
        print("✓ Database initialized successfully!")

def run_app():
    """Run the Flask application"""
    print("\n" + "="*50)
    print("🛡️  MFA Manager - TOTP Code Generator")
    print("="*50)
    host = '0.0.0.0' if os.environ.get('FLASK_ENV') == 'production' else '127.0.0.1'
    db_path = os.environ.get('DATABASE_PATH', 'mfa_manager.db')
    print(f"🌐 Server starting at: http://{host}:5000")
    print(f"📁 Database location: {os.path.abspath(db_path)}")
    print("="*50)
    print("🔒 Security Tips:")
    print("   • Keep your secret keys secure")
    print("   • Don't share TOTP codes")
    print("   • Run this on a secure device")
    print("   • Consider setting a SECRET_KEY environment variable")
    print("="*50)
    
    # Initialize database
    create_database()
    
    # Set configuration based on environment
    flask_env = os.environ.get('FLASK_ENV', 'development')
    is_production = flask_env == 'production'
    
    app.config['DEBUG'] = not is_production
    app.config['ENV'] = flask_env
    
    # Run the application
    try:
        host = '0.0.0.0' if is_production else '127.0.0.1'
        app.run(
            debug=not is_production,
            host=host,
            port=5000,
            use_reloader=not is_production
        )
    except KeyboardInterrupt:
        print("\n👋 MFA Manager stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")

if __name__ == '__main__':
    run_app()
