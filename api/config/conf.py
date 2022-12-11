from decouple import config
from pathlib import Path
import uuid

MODE = config("MODE")

IMPORT_PATH = Path("/import")
PKI_PATH = Path("/PKI")
KEYS_PATH = PKI_PATH / "private"
REQS_PATH = PKI_PATH / "reqs"
CONFIGS_PATH = PKI_PATH / "configs"
CONFIG_FILE = CONFIGS_PATH / "openssl.cnf"
CERTS_PATH = PKI_PATH / "certs"
PASSPRHASE_PATH = PKI_PATH / "private/_passphrase"
PUBLIC_PATH = PKI_PATH / "public"

CA_CRT_PATH = CERTS_PATH / "ca.crt"
CA_KEY_PATH = KEYS_PATH / "ca.key"
CA_PUB_PATH = PUBLIC_PATH / "ca.pub.pem"

CNF_BASE_DEFAULT = Path(__file__).parents[0] / "config/default.cnf"
CNF_BASE_OPENSSL = Path(__file__).parents[0] / "config/openssl.cnf"

# IMAGES AND MEDIA
###############################
# ASSETS_PATH = Path(__file__).parents[1] / "assets"
# IG_MEDIA_PATH = ASSETS_PATH / "images/ig/download"

# INSTAGRAM
###############################
# IG_TOKENS_PATH = Path(__file__).parents[1] / "lib/data/ig_tokens"
# IG_USER_IDS_FILE = Path("/run/secrets/ig_user_id")
# IG_CHECK_FREQ = config("IG_CHECK_FREQ", default=60, cast=int)
# IG_RENEW_FREQ = config("IG_RENEW_FREQ", default=43200, cast=int)

# JWT
###############################
# USER_NAMESPACE = uuid.UUID("6aaaa2c0-6254-4840-ae71-a73575121820")


