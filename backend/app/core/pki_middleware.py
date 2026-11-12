from pathlib import Path


def pki_middleware(PKI: Path):
    try:
        if not PKI.exists():
            return False
        is_empty = not any(PKI.iterdir())
        if is_empty:
            return False
        return True
    except Exception as e:
        return False
