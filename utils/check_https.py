#!/usr/bin/env python3
"""
Check if HTTPS setup is working
"""

import os
import requests
import ssl
import socket

def check_ssl_files():
    """Check if SSL certificate files exist"""
    cert_exists = os.path.exists('localhost.crt')
    key_exists = os.path.exists('localhost.key')
    
    print("🔒 SSL Certificate Status:")
    print(f"   Certificate file: {'✅' if cert_exists else '❌'} localhost.crt")
    print(f"   Private key file: {'✅' if key_exists else '❌'} localhost.key")
    
    return cert_exists and key_exists

def check_https_server():
    """Check if HTTPS server is running"""
    try:
        # Create SSL context that ignores certificate verification
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # Test HTTPS connection
        response = requests.get('https://localhost:5000/api/health', 
                              verify=False, timeout=5)
        
        if response.status_code == 200:
            print("✅ HTTPS server is running!")
            return True
        else:
            print(f"⚠️  HTTPS server responded with status: {response.status_code}")
            return False
            
    except requests.exceptions.SSLError:
        print("❌ SSL connection failed")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to HTTPS server")
        return False
    except Exception as e:
        print(f"❌ HTTPS test failed: {e}")
        return False

def main():
    """Main function"""
    print("🧪 HTTPS Setup Verification")
    print("=" * 40)
    
    # Check SSL files
    ssl_files_ok = check_ssl_files()
    
    if ssl_files_ok:
        print("\n🌐 Server Status:")
        https_ok = check_https_server()
        
        if https_ok:
            print("\n🎉 HTTPS is working!")
            print("📱 Access your demo at: https://localhost:5000")
            print("⚠️  Browser will show security warning - click 'Advanced' → 'Proceed to localhost'")
            print("\n✅ Your Spotify app should now work with:")
            print("   Redirect URI: https://localhost:5000/callback")
        else:
            print("\n❌ HTTPS server not responding")
            print("💡 Try restarting the Flask app")
    else:
        print("\n❌ SSL certificates not found")
        print("💡 Run: python ssl_cert.py")

if __name__ == "__main__":
    main() 