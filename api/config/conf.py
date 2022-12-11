from decouple import config
from pathlib import Path
import uuid

MODE = config("MODE")

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


