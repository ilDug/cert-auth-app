from pathlib import Path

def pki_middleware(pki_path: Path):
    try:
        if not pki_path.exists():
            return False
        is_empty = not any(pki_path.iterdir())
        if is_empty:
            return False
        return True
    except Exception as e:
        return False
