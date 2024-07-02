from fastapi import HTTPException
from core.config import PKI_PATH


def pki_middleware():
    cwd = PKI_PATH
    try:
        if not cwd.exists():
            return False
        is_empty = not any(cwd.iterdir())
        if is_empty:
            return False
        return True
    except Exception as e:
        return False
