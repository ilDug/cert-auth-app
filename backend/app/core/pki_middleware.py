from pathlib import Path


def pki_middleware(PKI: Path):
    try:
        if not PKI.exists():
            return False
        is_empty = not any(PKI.iterdir())
        return not is_empty
    except Exception:
        return False
