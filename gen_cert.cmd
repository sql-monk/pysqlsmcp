@echo off
REM Generate a self-signed certificate for local development
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
echo Done. Files created: cert.pem, key.pem
