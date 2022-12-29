from pathlib import Path


def remove_tmp_file(self, filename: Path):
    if filename.exists():
        filename.unlink()
