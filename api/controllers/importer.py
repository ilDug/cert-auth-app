from pathlib import Path
from .installer import Installer
import zipfile
from config.conf import PKI_PATH
from fastapi import HTTPException

class Importer(Installer):
    def __init__(self) -> None:
        super().__init__()

    def extract_pki(self, archive: Path):
        try:
            with zipfile.ZipFile(archive, mode="r") as zip_file:
                for file in zip_file.namelist():
                    zip_file.extract(file, PKI_PATH)
            return True
        except Exception:
            raise HTTPException(500, "impossibile estrare archivio")

    # def import_ca(self):
    #     crt = self.import_crt()
    #     key = self.import_key()

    #     if crt and key:
    #         CA_KEY_PATH.write_text(key.read_text())
    #         CA_CRT_PATH.write_text(crt.read_text())
    #         self.register_passphrase()
    #     else:
    #         typer.Exit("non sono stati trovati i file necessari all'importazione")

    # def import_crt(self) -> Path:
    #     for file in IMPORT_PATH.iterdir():
    #         if file.is_file() and file.suffix == ".crt":
    #             return file

    # def import_key(self) -> Path:
    #     for file in IMPORT_PATH.iterdir():
    #         if file.is_file() and file.suffix == ".key":
    #             return file

    # def register_passphrase(self):
    #     passphrase = typer.prompt("inserire la passphrase")
    #     PASSPRHASE_PATH.write_text(passphrase)
    #     PASSPRHASE_PATH.chmod(400)
