import ntplib
import ssl
import socket
import os
from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.x509.oid import NameOID

# Define the NTP server and port to use
ntp_server = 'time.cloudflare.com'
ntp_port = 1234

# Load the client's private key and certificate
with open('Assignment4\client.key', 'rb') as f:
    pem_data = f.read()
    private_key = serialization.load_pem_private_key(
        pem_data,
        password=None,  # Replace with password if the key is encrypted
    )

with open('Assignment4\client.crt', 'rb') as f:
    client_cert = x509.load_pem_x509_certificate(f.read())

# Create an SSL context with the client's private key and certificate
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_cert_chain(certfile='Assignment4\client.crt', keyfile='Assignment4\client.key')
ssl_context.options |= ssl.OP_NO_SSLv2
ssl_context.options |= ssl.OP_NO_SSLv3
ssl_context.options |= ssl.OP_NO_TLSv1
ssl_context.options |= ssl.OP_NO_TLSv1_1

# Create an NTP client and configure it for NTS
ntp_client = ntplib.NTPClient()
ntp_client.request('dns', 'pool.ntp.org', nts=True, port=1234)

# Create an NTS client to get a valid NTS cookie from the server
nts_client = ntp_client._nts_client
cookie = nts_client.get_cookie(ntp_server, ntp_port)

# Connect to the NTP server over TLS with NTS
with socket.create_connection((ntp_server, ntp_port)) as sock:
    wrapped_socket = ssl_context.wrap_socket(sock, server_hostname=ntp_server)
    wrapped_socket.sendall(cookie.to_bytes())
    wrapped_socket.sendall(ntp_client.request(ntp_server, version=4, nts=True).to_bytes())

    response = wrapped_socket.recv(1024)
    ntp_packet = ntplib.NTPPacket.from_bytes(response)

# Extract the time from the NTP response
ntp_time = ntp_packet.orig_timestamp
unix_time = ntp_time - ntplib.NTP_DELTA
gmt_time = datetime.utcfromtimestamp(unix_time)

# Print the current time in GMT format
print('Current GMT time:', gmt_time.strftime('%Y-%m-%d %H:%M:%S'))
