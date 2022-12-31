from pathlib import Path


def remove_tmp_file(filename: Path):
    if filename.exists():
        filename.unlink()
