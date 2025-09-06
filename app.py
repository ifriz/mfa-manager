from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, MFAAccount
import pyotp
import os
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
# Use environment variable for database path in Docker, fallback to current directory
database_path = os.environ.get('DATABASE_PATH', 'mfa_manager.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

@app.route('/')
def index():
    """Main dashboard showing all MFA accounts and their current codes"""
    accounts = MFAAccount.query.all()
    account_data = []
    
    for account in accounts:
        account_data.append({
            'id': account.id,
            'account_name': account.account_name,
            'issuer': account.issuer,
            'totp_code': account.get_totp_code(),
            'remaining_time': account.get_remaining_time()
        })
    
    return render_template('index.html', accounts=account_data)

@app.route('/add', methods=['GET', 'POST'])
def add_account():
    """Add a new MFA account"""
    if request.method == 'POST':
        account_name = request.form.get('account_name')
        secret = request.form.get('secret')
        issuer = request.form.get('issuer', 'MFA Manager')
        
        if not account_name or not secret:
            flash('Account name and secret are required!', 'error')
            return render_template('add_account.html')
        
        # Validate secret format
        try:
            # Try to create a TOTP object to validate the secret
            pyotp.TOTP(secret).now()
        except Exception as e:
            flash(f'Invalid secret format: {str(e)}', 'error')
            return render_template('add_account.html')
        
        # Check if account name already exists
        existing = MFAAccount.query.filter_by(account_name=account_name).first()
        if existing:
            flash('Account name already exists!', 'error')
            return render_template('add_account.html')
        
        # Create new account
        new_account = MFAAccount(
            account_name=account_name,
            secret=secret.upper().replace(' ', ''),  # Normalize secret
            issuer=issuer
        )
        
        try:
            db.session.add(new_account)
            db.session.commit()
            flash(f'Account "{account_name}" added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding account: {str(e)}', 'error')
    
    return render_template('add_account.html')

@app.route('/generate_secret')
def generate_secret():
    """Generate a random secret for testing purposes"""
    secret = pyotp.random_base32()
    return jsonify({'secret': secret})

@app.route('/account/<int:account_id>')
def view_account(account_id):
    """View details for a specific account including QR code"""
    account = MFAAccount.query.get_or_404(account_id)
    
    account_data = {
        'id': account.id,
        'account_name': account.account_name,
        'issuer': account.issuer,
        'secret': account.secret,
        'totp_code': account.get_totp_code(),
        'remaining_time': account.get_remaining_time(),
        'qr_code_image': account.generate_qr_code_image(),
        'qr_code_url': account.get_qr_code_url()
    }
    
    return render_template('account_detail.html', account=account_data)

@app.route('/delete/<int:account_id>', methods=['POST'])
def delete_account(account_id):
    """Delete an MFA account"""
    account = MFAAccount.query.get_or_404(account_id)
    account_name = account.account_name
    
    try:
        db.session.delete(account)
        db.session.commit()
        flash(f'Account "{account_name}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting account: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/edit/<int:account_id>', methods=['GET', 'POST'])
def edit_account(account_id):
    """Edit an existing MFA account"""
    account = MFAAccount.query.get_or_404(account_id)
    
    if request.method == 'POST':
        new_account_name = request.form.get('account_name')
        new_secret = request.form.get('secret')
        new_issuer = request.form.get('issuer', 'MFA Manager')
        
        if not new_account_name or not new_secret:
            flash('Account name and secret are required!', 'error')
            return render_template('edit_account.html', account=account)
        
        # Validate secret format
        try:
            pyotp.TOTP(new_secret).now()
        except Exception as e:
            flash(f'Invalid secret format: {str(e)}', 'error')
            return render_template('edit_account.html', account=account)
        
        # Check if new account name conflicts with existing (excluding current)
        if new_account_name != account.account_name:
            existing = MFAAccount.query.filter_by(account_name=new_account_name).first()
            if existing:
                flash('Account name already exists!', 'error')
                return render_template('edit_account.html', account=account)
        
        # Update account
        account.account_name = new_account_name
        account.secret = new_secret.upper().replace(' ', '')
        account.issuer = new_issuer
        
        try:
            db.session.commit()
            flash(f'Account "{new_account_name}" updated successfully!', 'success')
            return redirect(url_for('view_account', account_id=account.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating account: {str(e)}', 'error')
    
    return render_template('edit_account.html', account=account)

@app.route('/api/codes')
def get_all_codes():
    """API endpoint to get all current TOTP codes (for auto-refresh)"""
    accounts = MFAAccount.query.all()
    codes = []
    
    for account in accounts:
        codes.append({
            'id': account.id,
            'account_name': account.account_name,
            'totp_code': account.get_totp_code(),
            'remaining_time': account.get_remaining_time()
        })
    
    return jsonify(codes)

@app.route('/api/code/<int:account_id>')
def get_single_code(account_id):
    """API endpoint to get TOTP code for a specific account"""
    account = MFAAccount.query.get_or_404(account_id)
    
    return jsonify({
        'id': account.id,
        'account_name': account.account_name,
        'totp_code': account.get_totp_code(),
        'remaining_time': account.get_remaining_time()
    })

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # In production/Docker, bind to all interfaces
    host = '0.0.0.0' if os.environ.get('FLASK_ENV') == 'production' else '127.0.0.1'
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host=host, port=5000)
