#!/usr/bin/env python3
"""
JAEGIS Secret Key Generator
Generates secure encryption keys for S.C.R.I.P.T. framework
"""

import secrets
import base64
from cryptography.fernet import Fernet

def generate_jaegis_secret_key():
    """Generate a secure 32-character encryption key for JAEGIS_SECRET_KEY"""
    # Generate a Fernet-compatible key (32 bytes, base64 encoded)
    key = Fernet.generate_key()
    return key.decode('utf-8')

def generate_session_secret():
    """Generate a secure session secret key"""
    return secrets.token_urlsafe(32)

def generate_api_key():
    """Generate a secure API key"""
    return secrets.token_urlsafe(24)

def main():
    print("🔐 JAEGIS Security Key Generator")
    print("=" * 50)
    
    # Generate keys
    jaegis_key = generate_jaegis_secret_key()
    session_key = generate_session_secret()
    api_key = generate_api_key()
    
    print(f"JAEGIS_SECRET_KEY={jaegis_key}")
    print(f"SESSION_SECRET_KEY={session_key}")
    print(f"API_KEY={api_key}")
    print()
    print("📝 Instructions:")
    print("1. Copy these keys to your .env file")
    print("2. Keep these keys secure and never commit them to version control")
    print("3. Use different keys for different environments (dev/staging/prod)")
    print()
    print("⚠️  Security Notes:")
    print("- JAEGIS_SECRET_KEY is used for encrypting sensitive settings")
    print("- SESSION_SECRET_KEY is used for session management")
    print("- API_KEY can be used for API authentication")

if __name__ == "__main__":
    main()
