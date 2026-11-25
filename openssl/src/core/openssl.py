"""OpenSSL command definitions for passphrase generation."""

# openssl rand -base64 32 | tr -d '/.+'
PASSPHRASE = "openssl rand -base64 32"

PRIVATEKEY = "openssl genpkey -algorithm RSA -aes-256-cbc -pass pass:<passphrase> -pkeyopt rsa_keygen_bits:<bits> -out <output>"

