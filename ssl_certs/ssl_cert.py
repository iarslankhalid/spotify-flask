from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import ipaddress

# Generate key
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Create subject
subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])

# Create cert
cert = (x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(subject)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
    .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365))
    .add_extension(x509.SubjectAlternativeName([
        x509.DNSName("localhost"),
        x509.IPAddress(ipaddress.ip_address("127.0.0.1"))
    ]), critical=False)
    .sign(key, hashes.SHA256()))

# Write files
with open("localhost.key", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("localhost.crt", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("✅ SSL certificates created: localhost.key and localhost.crt") 