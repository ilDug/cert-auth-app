import json
from os import environ as env
from pathlib import Path


MODE = env["MODE"]
ROOT = Path("/app")

LIB = ROOT / "lib"

IMPORT_PATH = Path("/import")
PKI_PATH = Path("/PKI")


PKI_DB = PKI_PATH / "index.txt"
KEYS_PATH = PKI_PATH / "private"
REQS_PATH = PKI_PATH / "reqs"
CONFIGS_PATH = PKI_PATH / "configs"
CERTS_PATH = PKI_PATH / "certs"
PASSPRHASE_PATH = PKI_PATH / "private/_passphrase"
PUBLIC_PATH = PKI_PATH / "public"

CONFIG_FILE = CONFIGS_PATH / "openssl.cnf"
CA_CRT_PATH = CERTS_PATH / "ca.crt"
CA_KEY_PATH = KEYS_PATH / "ca.key"
CA_PUB_PATH = PUBLIC_PATH / "ca.pub.pem"
CA_DURATION = 365

CNF_BASE_DEFAULT = LIB / "openssl/default.cnf"
CNF_BASE_OPENSSL = LIB / "openssl/openssl.cnf"
