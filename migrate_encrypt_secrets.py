"""
Migration script to encrypt any existing plaintext MFA secrets in the database.
Run this script once after deploying the encryption update.
"""

from app import app, db
from models import MFAAccount
from sqlalchemy.exc import SQLAlchemyError
from cryptography.fernet import InvalidToken

def is_encrypted(secret):
    # Fernet tokens are always 128+ chars base64, but this is a heuristic
    try:
        MFAAccount._get_fernet().decrypt(secret.encode())
        return True
    except InvalidToken:
        return False
    except Exception:
        return False

def migrate_plaintext_secrets():
    with app.app_context():
        accounts = MFAAccount.query.all()
        updated = 0
        for account in accounts:
            try:
                # Try to decrypt; if fails, treat as plaintext
                MFAAccount._get_fernet().decrypt(account.secret.encode())
            except InvalidToken:
                # Not encrypted, so encrypt and update
                plaintext = account.secret
                account.secret = account.encrypt_secret(plaintext)
                updated += 1
            except Exception as e:
                print(f"Error processing account {account.account_name}: {e}")
        try:
            db.session.commit()
            print(f"Migration complete. {updated} account(s) updated.")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"DB error: {e}")

if __name__ == "__main__":
    migrate_plaintext_secrets()
