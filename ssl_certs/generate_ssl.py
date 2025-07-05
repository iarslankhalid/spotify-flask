#!/usr/bin/env python3
"""
Generate self-signed SSL certificate for localhost development
"""

import os
import subprocess
import sys
from pathlib import Path

def check_openssl():
    """Check if OpenSSL is available"""
    try:
        result = subprocess.run(['openssl', 'version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ OpenSSL found: {result.stdout.strip()}")
            return True
        else:
            print("❌ OpenSSL not found")
            return False
    except FileNotFoundError:
        print("❌ OpenSSL not found in PATH")
        return False

def generate_certificate():
    """Generate self-signed certificate for localhost"""
    print("🔐 Generating SSL certificate for localhost...")
    
    # Certificate configuration
    cert_file = "localhost.crt"
    key_file = "localhost.key"
    
    # Generate private key
    key_cmd = [
        'openssl', 'genrsa', 
        '-out', key_file, 
        '2048'
    ]
    
    # Generate certificate
    cert_cmd = [
        'openssl', 'req', '-new', '-x509',
        '-key', key_file,
        '-out', cert_file,
        '-days', '365',
        '-subj', '/C=US/ST=Demo/L=Demo/O=SpotifyMoodDemo/CN=localhost'
    ]
    
    try:
        # Generate private key
        print("🔑 Generating private key...")
        subprocess.run(key_cmd, check=True, capture_output=True)
        
        # Generate certificate
        print("📜 Generating certificate...")
        subprocess.run(cert_cmd, check=True, capture_output=True)
        
        print(f"✅ SSL certificate generated successfully!")
        print(f"   - Certificate: {cert_file}")
        print(f"   - Private key: {key_file}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating certificate: {e}")
        return False

def python_ssl_fallback():
    """Generate certificate using Python's built-in SSL if OpenSSL not available"""
    print("🐍 Using Python fallback method...")
    
    try:
        # Create a simple self-signed certificate using cryptography library
        print("📦 Installing cryptography library...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'cryptography'], 
                      check=True, capture_output=True)
        
        # Import after installation
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        import datetime
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Create certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Demo"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Demo"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "SpotifyMoodDemo"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress("127.0.0.1"),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Write private key
        with open("localhost.key", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        # Write certificate
        with open("localhost.crt", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        print("✅ SSL certificate generated using Python!")
        print("   - Certificate: localhost.crt")
        print("   - Private key: localhost.key")
        
        return True
        
    except Exception as e:
        print(f"❌ Python fallback failed: {e}")
        return False

def main():
    """Main function"""
    print("🔒 Setting up HTTPS for Spotify Mood Analyzer")
    print("=" * 50)
    
    # Check if files already exist
    if os.path.exists("localhost.crt") and os.path.exists("localhost.key"):
        print("ℹ️  SSL certificate already exists!")
        return True
    
    # Try OpenSSL first
    if check_openssl():
        success = generate_certificate()
    else:
        print("🔄 OpenSSL not found, trying Python fallback...")
        success = python_ssl_fallback()
    
    if success:
        print("\n🎉 HTTPS setup complete!")
        print("📝 Next steps:")
        print("   1. Update app.py to use SSL")
        print("   2. Access your app at: https://localhost:5000")
        print("   3. Accept the security warning in your browser")
    else:
        print("\n❌ Failed to generate SSL certificate")
        print("💡 Alternative: Update your Spotify app to use http://localhost:5000")

if __name__ == "__main__":
    main() 